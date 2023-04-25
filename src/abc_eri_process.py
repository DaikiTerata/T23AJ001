from abc import abstractmethod

from xgnlog.Log import Level

from src.abc_process import AbcProcess, Mode, SoutSeverity
from src.eri_connection import NFShellClient, ProxyCommandException, SocketTimeoutException, SSHConnectException
from src.eri_connection_stub import NFStubShellClient as StubClient


class AbcEricssonProcess(AbcProcess):
    """エリクソンNF抽象プロセスクラス

    """

    def __init__(self,
                 alias: str,
                 nf_name: str,
                 mode: Mode,
                 stub: bool,
                 job_id: str = None):
        """コンストラクタ

        Args:
            alias (str): エイリアス
            nf_name (str): NF名
            mode (Mode): 実行モード
            stub (bool): スタブ実行設定
            job_id (str, optional): JOBID. Defaults to None.
        """
        super().__init__(alias, nf_name, mode, job_id)
        self.__client = None
        if stub:
            self.__client = StubClient(mode, nf_name)
        else:
            self.__client = NFShellClient(nf_name)

    @property
    def client(self) -> NFShellClient:
        """接続クライアントプロパティを取得

        Returns:
            NFShellClient: 接続クライアント
        """
        return self.__client

    @abstractmethod
    def get_commit_comment(self, *args, **kwargs) -> str:
        """コミット時に適用するコミットコメントを取得する

        Returns:
            str: コミットコメント
        """
        pass

    def open_client(self) -> bool:
        """対向ノードとのSSHクライアント接続を開始

        Returns:
            bool: 接続成功ならTrue、失敗ならFalse
        """
        self.logger.output_1st_log("I00301", self.nf_name)

        try:
            self.client.connect()

            # 事前コマンド実行
            command = "screen-length 0"
            self.logger.output_1st_log("I00309", command)
            result = self.client.command(command).decode("utf-8")
            self.logger.output_1st_log("I00310", result)
        except KeyError as e:
            self.sout_message(SoutSeverity.error, "nf configuration not found.")
            self.logger.output_1st_log("E00301", self.nf_name)
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"NF設定取得エラー:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" Trace: {e.__class__.__name__} {e}")
            self.logger.output_1st_log("E00302", self.nf_name)
            return False
        except ProxyCommandException as e:
            self.sout_message(SoutSeverity.error, f"ssh bastion {str(e)} setting something wrong. [ UNKNOWN ]")
            self.logger.output_1st_log("E00303", self.nf_name)
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"ProxyCommand生成エラー:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" Trace: {e.__class__.__name__} {e}")
            self.logger.output_1st_log("E00302", self.nf_name)
            return False
        except SSHConnectException as e:
            self.client.close()
            self.sout_message(SoutSeverity.error, "ssh process coundn't connect to nf or bastion. [ UNKNOWN ]")
            self.logger.output_1st_log("E00304", self.nf_name)
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"SSH接続エラー:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" Trace: {e.__class__.__name__} {e}")
            return False
        except SocketTimeoutException as e:
            self.client.close()
            self.sout_message(SoutSeverity.error, "ssh connection timeout was happened. [ UNKNOWN ]")
            self.logger.output_1st_log("E00304", self.nf_name)
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"SSHタイムアウト発生:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" Trace: {e.__class__.__name__} {e}")
            return False

        self.logger.output_1st_log("I00302", self.nf_name)
        return True

    def close_client(self) -> None:
        """対向ノードとのSSHクライアントを切断

        Returns:
            None: なし
        """
        self.logger.output_1st_log("I00303", self.nf_name)
        self.client.close()
        self.logger.output_1st_log("I00304", self.nf_name)

    def commit(self) -> bool:
        """対象NFに対して変更内容を保存する

        Raises:
            ValueError: 正常性検証が正常に終了しなかった場合
            ValueError: 設定コミットが正常に終了しなかった場合

        Returns:
            bool: 正常終了完了ならTrue、例外発生ならFalse
        """
        self.logger.output_1st_log("I00305", self.nf_name)

        try:
            # 設定変更モード開始
            self.logger.output_1st_log("I00309", "config")
            self.client.enter_config_mode()
            self.logger.output_1st_log("I00310", None)

            # 差分確認
            command = "show configuration diff"
            self.logger.output_1st_log("I00309", command)
            result = self.client.command(command).decode("utf-8")
            self.logger.output_1st_log("I00310", result)

            # 正常性検証
            command = "validate"
            self.logger.output_1st_log("I00309", command)
            result = self.client.command(command).decode("utf-8")
            self.logger.output_1st_log("I00310", result)
            pattern = "Validation complete"
            if not result.count(pattern):
                raise ValueError("Validate for status change was failed.")

            # 設定投入
            command = f"commit comment {self.get_commit_comment()}"
            self.logger.output_1st_log("I00309", command)
            result = self.client.command(command).decode("utf-8")
            self.logger.output_1st_log("I00310", result)
            pattern = "Commit complete"
            if not result.count(pattern):
                raise ValueError("Commit for status change was failed.")

            # 設定変更モード終了
            self.logger.output_1st_log("I00309", "end")
            self.client.exit_config_mode()
            self.logger.output_1st_log("I00310", None)

        except SocketTimeoutException as e:
            # タイムアウト発生の旨を表示
            self.sout_message(SoutSeverity.error, "ssh connection timeout was happened. [ UNKNOWN ]")
            self.logger.output_1st_log("E00303", [self.nf_name, self.mode])
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"変更反映異常:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" コマンド: {command}\n"
                                       f" Trace: {e.__class__.__name__} {e}")
            return False
        except Exception as e:
            self.sout_message(SoutSeverity.error, "unexpected error occurred. [ UNKNOWN ]")
            self.logger.output_1st_log("E00303", [self.nf_name, self.mode])
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"変更反映異常:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" コマンド: {command}\n"
                                       f" Trace: {e.__class__.__name__} {e}")
            return False

        self.logger.output_1st_log("I00306", self.nf_name)
        return True

    def do_abort(self) -> bool:
        """コマンドエラー発生時に設定を元に戻す

        Returns:
            bool: 元に戻すが正常に完了したらTrue、何らかの異常が発生したらFalse
        """
        self.logger.output_1st_log("I00307", self.nf_name)

        try:
            self.logger.output_1st_log("I00309", "abort")
            self.client.abort()
            self.logger.output_1st_log("I00310", None)
        except Exception as e:
            self.sout_message(SoutSeverity.error, "unexpected error occurred. [ UNKNOWN ]")
            self.logger.output_1st_log("E00305", self.nf_name)
            self.logger.output_2nd_log(Level.CRITICAL,
                                       f"ABORTコマンド実行異常:\n"
                                       "パラメータ:\n"
                                       f" NF名: {self.nf_name}\n"
                                       f" Trace: {e.__class__.__name__} {e}")
            return False

        self.logger.output_1st_log("I00308", self.nf_name)
        return True
