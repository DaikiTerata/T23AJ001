import pathlib
from typing import Any, List
from datetime import datetime

import pytest
from pytest_mock import MockerFixture
from xgnlog.Log import Level

from src.abc_eri_process import AbcEricssonProcess
from src.abc_process import Mode, ProcessStatus, TargetStatus
from src.eri_connection import ProxyCommandException, SSHConnectException, SocketTimeoutException

JOB_ID = "T23AJ003"


def get_1st_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("1st_abc_eri_process.log")


def get_2nd_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("2nd_abc_eri_process.log")


class MockLog():
    def __init__(self, job_id: str, init_level: Level, log_dir: str) -> None:
        self.job_id = job_id
        self.init_level = init_level
        self.log_path_1st = get_1st_log_path(log_dir)
        self.log_path_2nd = get_2nd_log_path(log_dir)

    def output_1st_log(self, msg_id: str, add_info: Any = None) -> None:
        with open(self.log_path_1st, "a", encoding="utf-8", newline="\n") as f:
            f.write("job_id:{0}, message_id:{1}, add_info:{2}\n".format(self.job_id, msg_id, add_info))

    def output_2nd_log(self, level: Level, add_info: Any = None) -> None:
        with open(self.log_path_2nd, "a", encoding="utf-8", newline="\n") as f:
            f.write("job_id:{0}, level:{1}, add_info:{2}\n".format(self.job_id, level.name, add_info))


class MockABC(AbcEricssonProcess):
    def change_status(self, *args, **kwargs) -> ProcessStatus:
        pass

    def changed_check(self, status: TargetStatus) -> ProcessStatus:
        pass

    def get_commit_comment(self) -> str:
        pass

    def get_status(self) -> TargetStatus:
        pass

    def get_status_word(self, status: TargetStatus) -> str:
        pass

    def necessity_check(self, status: TargetStatus) -> ProcessStatus:
        pass

    def post_check(self, *args, **kwargs) -> bool:
        pass

    def pre_check(self, *args, **kwargs) -> bool:
        pass

    def to_down(self) -> bool:
        pass

    def to_up(self) -> bool:
        pass

    def run(self) -> ProcessStatus:
        pass


class ClientForTest():
    def __init__(self, name: str):
        pass


class StubClientForTest():
    def __init__(self, mode: Mode, name: str):
        pass


def test_init01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_init01 __init__試験01 インスタンス生成(stub: False)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False

    試験結果
    ・インスタンス生成が正常に終了すること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcProcess__logger = logger

    client = process.client

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, MockABC)
    assert isinstance(client, ClientForTest)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_init02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_init02 __init__試験02 インスタンス生成(stub: True)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = True

    試験結果
    ・インスタンス生成が正常に終了すること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = True

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcProcess__logger = logger

    client = process.client

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, MockABC)
    assert isinstance(client, StubClientForTest)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_open_client01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_open_client01 open_client試験01 正常系試験

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・client.connectが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00301, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:screen-length 0\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:\n",
        f"job_id:{JOB_ID}, message_id:I00302, add_info:{nf_name}\n",
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.connect = mocker.Mock(side_effect=[True])
    test_mocker.command = mocker.Mock(side_effect=[b""])
    test_mocker.out_message = mocker.Mock(return_value=True)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    response_value = process.open_client()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.connect.called == True
    assert test_mocker.connect.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_open_client02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_open_client02 open_client試験02 異常系試験(KeyError)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False
    ・KeyError発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・client.connectが1回呼ばれること
    ・client.commandが呼ばれないこと
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{alias}({nf_name}):nf configuration not found.\n".format(mode=mode, time=logtime_str, alias=alias, nf_name=nf_name)
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00301, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:E00301, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:E00302, add_info:{nf_name}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:NF設定取得エラー:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        " Trace: KeyError 'Test KeyError'\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.connect = mocker.Mock(side_effect=[KeyError("Test KeyError")])
    test_mocker.command = mocker.Mock(side_effect=[b""])
    test_mocker.out_message = mocker.Mock(return_value=True)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    response_value = process.open_client()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.connect.called == True
    assert test_mocker.connect.call_count == 1
    assert test_mocker.command.called == False
    assert test_mocker.command.call_count == 0
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_open_client03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_open_client03 open_client試験03 異常系試験 (ProxyCommandException)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False
    ・ProxyCommandException発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・client.connectが1回呼ばれること
    ・client.commandが呼ばれないこと
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False
    bastion = "director-1-a1-er-s01-vm-002"

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{alias}({nf_name}):ssh bastion {0} setting something wrong. [ UNKNOWN ]\n".format(bastion, mode=mode, time=logtime_str, alias=alias, nf_name=nf_name)
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00301, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:E00303, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:E00302, add_info:{nf_name}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:ProxyCommand生成エラー:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" Trace: ProxyCommandException {bastion}\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.connect = mocker.Mock(side_effect=[ProxyCommandException(bastion)])
    test_mocker.command = mocker.Mock(side_effect=[b""])
    test_mocker.out_message = mocker.Mock(return_value=True)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    response_value = process.open_client()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.connect.called == True
    assert test_mocker.connect.call_count == 1
    assert test_mocker.command.called == False
    assert test_mocker.command.call_count == 0
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_open_client04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_open_client04 open_client試験04 異常系試験 (SSHConnectException)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False
    ・SSHConnectException発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・client.connectが1回呼ばれること
    ・client.commandが呼ばれないこと
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{alias}({nf_name}):ssh process coundn't connect to nf or bastion. [ UNKNOWN ]\n".format(mode=mode, time=logtime_str, alias=alias, nf_name=nf_name)
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00301, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:E00304, add_info:{nf_name}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:SSH接続エラー:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" Trace: SSHConnectException Test SSHConnectException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.connect = mocker.Mock(side_effect=[SSHConnectException("Test SSHConnectException")])
    test_mocker.command = mocker.Mock(side_effect=[b""])
    test_mocker.out_message = mocker.Mock(return_value=True)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    response_value = process.open_client()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.connect.called == True
    assert test_mocker.connect.call_count == 1
    assert test_mocker.command.called == False
    assert test_mocker.command.call_count == 0
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_open_client05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_open_client05 open_client試験05 異常系試験 (SocketTimeoutException)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False
    ・SocketTimeoutException発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・client.connectが1回呼ばれること
    ・client.commandが呼ばれないこと
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{alias}({nf_name}):ssh connection timeout was happened. [ UNKNOWN ]\n".format(mode=mode, time=logtime_str, alias=alias, nf_name=nf_name)
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00301, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:E00304, add_info:{nf_name}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:SSHタイムアウト発生:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" Trace: SocketTimeoutException Test SocketTimeoutException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.connect = mocker.Mock(side_effect=[SocketTimeoutException("Test SocketTimeoutException")])
    test_mocker.command = mocker.Mock(side_effect=[b""])
    test_mocker.out_message = mocker.Mock(return_value=True)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    response_value = process.open_client()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.connect.called == True
    assert test_mocker.connect.call_count == 1
    assert test_mocker.command.called == False
    assert test_mocker.command.call_count == 0
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_close_client01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_close_client01 close_client試験01 正常系試験

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・client.closeが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    expected_value = None

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00303, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00304, add_info:{nf_name}\n",
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.close = mocker.Mock(return_value=True)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    response_value = process.close_client()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.close.called == True
    assert test_mocker.close.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_commit01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_commit01 commit試験01 正常系試験 (OK, deregistered)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・client.enter_config_modeが1回呼ばれること
    ・client.commandが3回呼ばれること
    ・client.exit_config_modeが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False

    after_status = TargetStatus.down
    commit_comment = "deregistered"

    command_response_value = [
        "\n".encode("utf-8"),  # show conf diff
        "Validation complete\n".encode("utf-8"),  # validate
        "Commit complete\n".encode("utf-8")  # commit
    ]

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00305, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:config\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:show configuration diff\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[0].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:I00309, add_info:validate\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[1].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:I00309, add_info:commit comment {commit_comment}\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[2].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:I00309, add_info:end\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00306, add_info:{nf_name}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.exit_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[*command_response_value])
    test_mocker.get_commit_comment = mocker.Mock(return_value=f"{commit_comment}")

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.after_status = after_status
    mocker.patch.object(process, "get_commit_comment", test_mocker.get_commit_comment)

    response_value = process.commit()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.enter_config_mode.called == True
    assert test_mocker.enter_config_mode.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 3
    assert test_mocker.exit_config_mode.called == True
    assert test_mocker.exit_config_mode.call_count == 1
    assert test_mocker.get_commit_comment.called == True
    assert test_mocker.get_commit_comment.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_commit02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_commit02 commit試験02 正常系試験 (OK, registered)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・client.enter_config_modeが1回呼ばれること
    ・client.commandが3回呼ばれること
    ・client.exit_config_modeが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    stub = False

    after_status = TargetStatus.up
    commit_comment = "registered"

    command_response_value = [
        "\n".encode("utf-8"),  # show conf diff
        "Validation complete\n".encode("utf-8"),  # validate
        "Commit complete\n".encode("utf-8")  # commit
    ]

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00305, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:config\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:show configuration diff\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[0].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:I00309, add_info:validate\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[1].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:I00309, add_info:commit comment {commit_comment}\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[2].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:I00309, add_info:end\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00306, add_info:{nf_name}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.exit_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[*command_response_value])
    test_mocker.get_commit_comment = mocker.Mock(return_value=f"{commit_comment}")

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.after_status = after_status
    mocker.patch.object(process, "get_commit_comment", test_mocker.get_commit_comment)

    response_value = process.commit()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.enter_config_mode.called == True
    assert test_mocker.enter_config_mode.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 3
    assert test_mocker.exit_config_mode.called == True
    assert test_mocker.exit_config_mode.call_count == 1
    assert test_mocker.get_commit_comment.called == True
    assert test_mocker.get_commit_comment.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_commit03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_commit03 commit試験03 異常系試験 (NG, SocketTimeoutException)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・stub = False
    ・SocketTimeoutException発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・client.enter_config_modeが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・client.exit_config_modeが0回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False

    after_status = TargetStatus.down
    commit_comment = "commit_comment"

    command_response_value = [
        "\n".encode("utf-8"),  # show conf diff
        "Validation complete\n".encode("utf-8"),  # validate
        "Commit error\n".encode("utf-8")  # commit
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{alias}({nf_name}):ssh connection timeout was happened. [ UNKNOWN ]\n".format(mode=mode, time=logtime_str, alias=alias, nf_name=nf_name)
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00305, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:config\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:show configuration diff\n",
        f"job_id:{JOB_ID}, message_id:E00303, add_info:{[nf_name, mode]}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:変更反映異常:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: show configuration diff\n",
        f" Trace: SocketTimeoutException Test SocketTimeoutException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.exit_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[SocketTimeoutException("Test SocketTimeoutException")])
    test_mocker.get_commit_comment = mocker.Mock(return_value=f"{commit_comment}")

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.after_status = after_status
    mocker.patch.object(process, "get_commit_comment", test_mocker.get_commit_comment)

    response_value = process.commit()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.enter_config_mode.called == True
    assert test_mocker.enter_config_mode.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert test_mocker.exit_config_mode.called == False
    assert test_mocker.exit_config_mode.call_count == 0
    assert test_mocker.get_commit_comment.called == False
    assert test_mocker.get_commit_comment.call_count == 0
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_commit04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_commit04 commit試験04 異常系試験 (NG, Validation error)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False
    ・Validation時にエラー発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・client.enter_config_modeが1回呼ばれること
    ・client.commandが2回呼ばれること
    ・client.exit_config_modeが0回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    after_status = TargetStatus.down
    commit_comment = "commit_comment"

    command_response_value = [
        "\n".encode("utf-8"),  # show conf diff
        "Validation error\n".encode("utf-8")  # validate
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{alias}({nf_name}):unexpected error occurred. [ UNKNOWN ]\n".format(mode=mode, time=logtime_str, alias=alias, nf_name=nf_name)
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00305, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:config\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:show configuration diff\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[0].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:I00309, add_info:validate\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[1].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:E00303, add_info:{[nf_name, mode]}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:変更反映異常:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: validate\n",
        f" Trace: ValueError Validate for status change was failed.\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.exit_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[*command_response_value])
    test_mocker.get_commit_comment = mocker.Mock(return_value=f"{commit_comment}")

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    mocker.patch.object(process, "get_commit_comment", test_mocker.get_commit_comment)

    response_value = process.commit()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.enter_config_mode.called == True
    assert test_mocker.enter_config_mode.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 2
    assert test_mocker.exit_config_mode.called == False
    assert test_mocker.exit_config_mode.call_count == 0
    assert test_mocker.get_commit_comment.called == False
    assert test_mocker.get_commit_comment.call_count == 0
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_commit05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_commit05 commit試験05 異常系試験 (NG, Commit error)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False
    ・Commit時にエラー発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・client.enter_config_modeが1回呼ばれること
    ・client.commandが3回呼ばれること
    ・client.exit_config_modeが0回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    after_status = TargetStatus.down
    commit_comment = "commit_comment"

    command_response_value = [
        "\n".encode("utf-8"),  # show conf diff
        "Validation complete\n".encode("utf-8"),  # validate
        "Commit error\n".encode("utf-8")  # commit
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{alias}({nf_name}):unexpected error occurred. [ UNKNOWN ]\n".format(mode=mode, time=logtime_str, alias=alias, nf_name=nf_name)
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00305, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:config\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:show configuration diff\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[0].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:I00309, add_info:validate\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[1].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:I00309, add_info:commit comment {commit_comment}\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[2].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:E00303, add_info:{[nf_name, mode]}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:変更反映異常:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: commit comment {commit_comment}\n",
        f" Trace: ValueError Commit for status change was failed.\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.exit_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[*command_response_value])
    test_mocker.get_commit_comment = mocker.Mock(return_value=f"{commit_comment}")

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.after_status = after_status
    mocker.patch.object(process, "get_commit_comment", test_mocker.get_commit_comment)

    response_value = process.commit()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.enter_config_mode.called == True
    assert test_mocker.enter_config_mode.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 3
    assert test_mocker.exit_config_mode.called == False
    assert test_mocker.exit_config_mode.call_count == 0
    assert test_mocker.get_commit_comment.called == True
    assert test_mocker.get_commit_comment.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_do_abort01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_do_abort01 do_abort試験01 正常系試験 (OK)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・client.abortが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False

    command_response_value = [
        None
    ]

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00307, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:abort\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00308, add_info:{nf_name}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.abort = mocker.Mock(side_effect=[*command_response_value])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    response_value = process.do_abort()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.abort.called == True
    assert test_mocker.abort.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_do_abort02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_do_abort02 do_abort試験02 異常系試験 (NG, SocketTimeoutException発生)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False
    ・SocketTimeoutException発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・client.abortが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定している内容であること
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False

    command_response_value = [
        None
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{alias}({nf_name}):unexpected error occurred. [ UNKNOWN ]\n".format(mode=mode, time=logtime_str, alias=alias, nf_name=nf_name)
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00307, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:abort\n",
        f"job_id:{JOB_ID}, message_id:E00305, add_info:{nf_name}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:ABORTコマンド実行異常:\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" Trace: SocketTimeoutException Test SocketTimeoutException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.abort = mocker.Mock(side_effect=[SocketTimeoutException("Test SocketTimeoutException")])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    response_value = process.do_abort()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.abort.called == True
    assert test_mocker.abort.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd
