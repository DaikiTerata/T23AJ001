import pathlib
from typing import Any, List
import pytest
from pytest_mock import MockerFixture
from datetime import datetime

from xgnlog.Log import Level
from src.abc_eri_process import AbcEricssonRegistrationProcess
from src.abc_process import ProcessStatus, Status
from src.eri_connection import ProxyCommandException, SSHConnectException, SocketTimeoutException

from src.xcap_common import Mode

JOB_ID = "T22AJ003"


def get_1st_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("1st_abc_eri_reg_process.log")


def get_2nd_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("2nd_abc_eri_reg_process.log")


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


class MockABC(AbcEricssonRegistrationProcess):
    def get_status(self) -> Status:
        pass

    def do_deregistered(self) -> bool:
        pass

    def do_registered(self) -> bool:
        pass

    def get_disp_status(self, status: Status) -> str:
        pass

    def run(self) -> ProcessStatus:
        pass


class TestClient():
    def __init__(self, name: str):
        pass


class TestStubClient():
    def __init__(self, mode: Mode, name: str):
        pass


def test_init01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_init01 __init__試験01 インスタンス生成(stub: False)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False

    試験結果
    ・インスタンス生成が正常に終了すること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    process = MockABC(edns_host, nf_name, mode, stub)
    client = process.client

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, MockABC)
    assert isinstance(client, TestClient)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_init02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_init02 __init__試験02 インスタンス生成(stub: True)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = True

    試験結果
    ・インスタンス生成が正常に終了すること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = True

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    process = MockABC(edns_host, nf_name, mode, stub)
    client = process.client

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, MockABC)
    assert isinstance(client, TestStubClient)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_open_client01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_open_client01 open_client試験01 正常系試験

    試験条件
    ・edns_host = "b1-CPA_East-Act"
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
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00314", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "screen-length 0"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", ""),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00315", nf_name),
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.connect = mocker.Mock(side_effect=[True])
    test_mocker.command = mocker.Mock(side_effect=[b""])
    test_mocker.out_message = mocker.Mock(return_value=True)

    process = MockABC(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker

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
    ・edns_host = "b1-CPA_East-Act"
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
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):nf configuration not found.\n".format(mode=mode, time=logtime_str, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00314", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00308", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00306", nf_name)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:NF設定取得エラー:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        " Trace: KeyError 'Test KeyError'\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.connect = mocker.Mock(side_effect=[KeyError("Test KeyError")])
    test_mocker.command = mocker.Mock(side_effect=[b""])
    test_mocker.out_message = mocker.Mock(return_value=True)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker

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
    ・edns_host = "b1-CPA_East-Act"
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
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False
    bastion = "director-1-a1-er-s01-vm-002"

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):ssh bastion {0} setting something wrong. [ UNKNOWN ]\n".format(bastion, mode=mode, time=logtime_str, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00314", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00308", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00306", nf_name)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:ProxyCommand生成エラー:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" Trace: ProxyCommandException {bastion}\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.connect = mocker.Mock(side_effect=[ProxyCommandException(bastion)])
    test_mocker.command = mocker.Mock(side_effect=[b""])
    test_mocker.out_message = mocker.Mock(return_value=True)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker

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
    ・edns_host = "b1-CPA_East-Act"
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
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):ssh process coundn't connect to nf or bastion. [ UNKNOWN ]\n".format(mode=mode, time=logtime_str, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00314", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00307", nf_name)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:SSH接続エラー:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" Trace: SSHConnectException Test SSHConnectException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.connect = mocker.Mock(side_effect=[SSHConnectException("Test SSHConnectException")])
    test_mocker.command = mocker.Mock(side_effect=[b""])
    test_mocker.out_message = mocker.Mock(return_value=True)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker

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
    ・edns_host = "b1-CPA_East-Act"
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
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):ssh connection timeout was happened. [ UNKNOWN ]\n".format(mode=mode, time=logtime_str, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00314", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00307", nf_name)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:SSHタイムアウト発生:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" Trace: SocketTimeoutException Test SocketTimeoutException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.connect = mocker.Mock(side_effect=[SocketTimeoutException("Test SocketTimeoutException")])
    test_mocker.command = mocker.Mock(side_effect=[b""])
    test_mocker.out_message = mocker.Mock(return_value=True)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker

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
    ・edns_host = "b1-CPA_East-Act"
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
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    expected_value = None

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00316", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00317", nf_name),
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.close = mocker.Mock(return_value=True)

    process = MockABC(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker

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
    ・edns_host = "b1-CPA_East-Act"
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
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False

    after_status = Status.down
    after_disp = "deregistered"

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
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00318", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "config"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "show configuration diff"),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[0].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "validate"),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[1].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", f"commit comment nf-status_{after_disp}"),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[2].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "end"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00319", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.exit_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[*command_response_value])
    test_mocker.get_disp_status = mocker.Mock(return_value=after_disp)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    process.after_status = after_status
    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

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
    assert test_mocker.get_disp_status.called == True
    assert test_mocker.get_disp_status.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_commit02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_commit02 commit試験02 正常系試験 (OK, registered)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
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
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    stub = False

    after_status = Status.up
    after_disp = "registered"

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
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00318", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "config"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "show configuration diff"),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[0].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "validate"),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[1].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", f"commit comment nf-status_{after_disp}"),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[2].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "end"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00319", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.exit_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[*command_response_value])
    test_mocker.get_disp_status = mocker.Mock(return_value=after_disp)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    process.after_status = after_status
    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

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
    assert test_mocker.get_disp_status.called == True
    assert test_mocker.get_disp_status.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_commit03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_commit03 commit試験03 異常系試験 (NG, SocketTimeoutException)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
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
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False

    after_status = Status.down
    after_disp = "deregistered"

    command_response_value = [
        "\n".encode("utf-8"),  # show conf diff
        "Validation complete\n".encode("utf-8"),  # validate
        "Commit error\n".encode("utf-8")  # commit
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):ssh connection timeout was happened. [ UNKNOWN ]\n".format(mode=mode, time=logtime_str, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00318", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "config"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "show configuration diff"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00308", [nf_name, mode])
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:変更反映異常(timeout):\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: show configuration diff\n",
        f" Trace: SocketTimeoutException Test SocketTimeoutException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.exit_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[SocketTimeoutException("Test SocketTimeoutException")])
    test_mocker.get_disp_status = mocker.Mock(return_value=after_disp)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    process.after_status = after_status
    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

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
    assert test_mocker.get_disp_status.called == False
    assert test_mocker.get_disp_status.call_count == 0
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_commit04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_commit04 commit試験04 異常系試験 (NG, Validation error)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
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
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    after_status = Status.down
    after_disp = "deregistered"

    command_response_value = [
        "\n".encode("utf-8"),  # show conf diff
        "Validation error\n".encode("utf-8")  # validate
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00318", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "config"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "show configuration diff"),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[0].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "validate"),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[1].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00308", [nf_name, mode])
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:変更反映異常(other):\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: validate\n",
        f" Trace: ValueError Validate for status change was failed.\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.exit_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[*command_response_value])
    test_mocker.get_disp_status = mocker.Mock(return_value=after_disp)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

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
    assert test_mocker.get_disp_status.called == False
    assert test_mocker.get_disp_status.call_count == 0
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_commit05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_commit05 commit試験05 異常系試験 (NG, Commit error)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
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
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    after_status = Status.down
    after_disp = "deregistered"

    command_response_value = [
        "\n".encode("utf-8"),  # show conf diff
        "Validation complete\n".encode("utf-8"),  # validate
        "Commit error\n".encode("utf-8")  # commit
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00318", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "config"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "show configuration diff"),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[0].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "validate"),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[1].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", f"commit comment nf-status_{after_disp}"),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[2].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00308", [nf_name, mode])
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:変更反映異常(other):\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: commit comment nf-status_{after_disp}\n",
        f" Trace: ValueError Commit for status change was failed.\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.exit_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[*command_response_value])
    test_mocker.get_disp_status = mocker.Mock(return_value=after_disp)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    process.after_status = after_status
    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

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
    assert test_mocker.get_disp_status.called == True
    assert test_mocker.get_disp_status.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_do_abort01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_do_abort01 do_abort試験01 正常系試験 (OK)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
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
    edns_host = "b1-CPA_East-Act"
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
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00320", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "abort"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00321", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.abort = mocker.Mock(side_effect=[*command_response_value])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

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
    ・edns_host = "b1-CPA_East-Act"
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
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False

    command_response_value = [
        None
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00320", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "abort"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00309", nf_name)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:ABORTコマンド実行異常:\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" Trace: SocketTimeoutException Test SocketTimeoutException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.abort = mocker.Mock(side_effect=[SocketTimeoutException("Test SocketTimeoutException")])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

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
