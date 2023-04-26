import pathlib
from typing import Any, List
from datetime import datetime

import pytest
from pytest_mock import MockerFixture
from xgnlog.Log import Level, Log

import src.abc_process
from src.abc_process import AbcProcess, Mode, ProcessStatus, SoutSeverity, TargetStatus

JOB_ID = "T23AJ003"


def get_1st_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("1st_abc_process.log")


def get_2nd_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("2nd_abc_process.log")


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


class MockABC(AbcProcess):
    def commit(self) -> bool:
        pass

    def do_abort(self) -> bool:
        pass

    def get_status(self) -> TargetStatus:
        pass

    def get_status_word(self, status: TargetStatus) -> str:
        pass

    def run(self) -> ProcessStatus:
        pass

    def to_down(self) -> bool:
        pass

    def to_up(self) -> bool:
        pass


def test_Status01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_Status01 Status試験01 Enum取得

    試験条件
    ・status = Status.up
    ・value = "UP"

    試験結果
    ・値が取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    status = TargetStatus.up
    value = TargetStatus.up.value

    expected_value = value

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    response_value = str(status)

    assert response_value == expected_value


def test_SoutSeverity01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_SoutSeverity01 SoutSeverity試験01 Enum取得

    試験条件
    ・severity = SoutSeverity.success
    ・value = "[SUCCESS]"

    試験結果
    ・値が取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    severity = SoutSeverity.success
    value = "[SUCCESS]"

    expected_value = value

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    response_value = str(severity)

    assert response_value == expected_value


def test_logtime01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_logtime01 ログ表示時間取得試験01

    """
    expected_value = "1994-12-03 12:34:56"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
    ]

    expected_log_1st = [
    ]

    expected_log_2nd = [
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    response_value = src.abc_process.logtime()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert date_mock.now.called == True
    assert date_mock.now.call_count == 1
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_init01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_init01 __init__試験01 インスタンス生成

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show

    試験結果
    ・インスタンス生成が正常に終了すること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    process = MockABC(alias, nf_name, mode, JOB_ID)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, MockABC)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_alias01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_alias01 alias試験01 aliasプロパティ取得

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show

    試験結果
    ・インスタンス生成が正常に終了すること
    ・aliasが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show

    expected_value = alias

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    process = MockABC(alias, nf_name, mode, JOB_ID)

    response_value = process.alias

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_nf_name01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_nf_name01 nf_name試験01 nf_nameプロパティ取得

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show

    試験結果
    ・インスタンス生成が正常に終了すること
    ・nf_nameが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show

    expected_value = nf_name

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    process = MockABC(alias, nf_name, mode, JOB_ID)

    response_value = process.nf_name

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_mode01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_mode01 mode試験01 modeプロパティ取得

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show

    試験結果
    ・インスタンス生成が正常に終了すること
    ・modeが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show

    expected_value = mode

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    process = MockABC(alias, nf_name, mode, JOB_ID)

    response_value = process.mode

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_mode01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_mode01 mode試験01 modeプロパティ取得

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show

    試験結果
    ・インスタンス生成が正常に終了すること
    ・modeが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show

    expected_value = mode

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    process = MockABC(alias, nf_name, mode, JOB_ID)

    response_value = process.mode

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_after_status01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_after_status01 after_status試験01 after_statusプロパティ取得

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・after_status = target.Status.up

    試験結果
    ・インスタンス生成が正常に終了すること
    ・after_statusが保存できること
    ・after_statusが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    after_status = TargetStatus.down

    expected_value = after_status

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    process = MockABC(alias, nf_name, mode, JOB_ID)

    process.after_status = after_status
    response_value = process.after_status

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_necessity01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_necessity01 necessity試験01 necessityプロパティ取得

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・necessity = true

    試験結果
    ・インスタンス生成が正常に終了すること
    ・necessityが保存できること
    ・necessityが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    necessity = True

    expected_value = necessity

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    process = MockABC(alias, nf_name, mode, JOB_ID)

    process.necessity = necessity
    response_value = process.necessity

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_logger01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_logger01 logger試験01 loggerプロパティ取得

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = True

    試験結果
    ・インスタンス生成が正常に終了すること
    ・loggerが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = True
    changed = True

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    process = MockABC(alias, nf_name, mode, JOB_ID)

    response_value = process.logger

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcProcess)
    assert isinstance(response_value, Log)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_logger02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_logger02 logger試験02 loggerプロパティ取得

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = True

    試験結果
    ・インスタンス生成が正常に終了すること
    ・loggerが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = True
    changed = True

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    process = MockABC(alias, nf_name, mode)

    response_value = process.logger

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcProcess)
    assert isinstance(response_value, AbcProcess.LogStub)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_changed01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_changed01 changed試験01 changedプロパティ取得

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・changed = True

    試験結果
    ・インスタンス生成が正常に終了すること
    ・changedが保存できること
    ・changedが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    changed = True

    expected_value = changed

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    process = MockABC(alias, nf_name, mode, JOB_ID)

    process.changed = changed
    response_value = process.changed

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_sout_message01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_sout_message01 sout_message試験06 異常系試験 (severity: SoutSeverity.success)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がNoneとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    status = TargetStatus.unknown
    severity = SoutSeverity.success
    body = "test message"

    command_response_value = []

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[SUCCESS]:{mode}:{time}:{alias}({nf_name}):".format(mode=mode, time=logtime, alias=alias, nf_name=nf_name) + "test message\n"
    ]

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    response_value = process.sout_message(severity, body)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_pre_check01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_pre_check01 pre_check試験01 正常系試験 (before_status: Status.down, necessity: True)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・before_status = Status.down
    ・necessity = True

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    before_status = TargetStatus.down
    necessity = True

    command_response_value = []

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status = mocker.Mock(return_value=before_status)
    test_mocker.necessity_check = mocker.Mock(return_value=necessity)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status", test_mocker.get_status)
    mocker.patch.object(process, "necessity_check", test_mocker.necessity_check)

    response_value = process.pre_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert test_mocker.get_status.called == True
    assert test_mocker.get_status.call_count == 1
    assert test_mocker.necessity_check.called == True
    assert test_mocker.necessity_check.call_count == 1
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_pre_check02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_pre_check02 pre_check試験02 正常系試験 (before_status: Status.down, necessity: False)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・before_status = Status.down
    ・necessity = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    before_status = TargetStatus.down
    necessity = False

    command_response_value = []

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status = mocker.Mock(return_value=before_status)
    test_mocker.necessity_check = mocker.Mock(return_value=necessity)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status", test_mocker.get_status)
    mocker.patch.object(process, "necessity_check", test_mocker.necessity_check)

    response_value = process.pre_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert test_mocker.get_status.called == True
    assert test_mocker.get_status.call_count == 1
    assert test_mocker.necessity_check.called == True
    assert test_mocker.necessity_check.call_count == 1
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_pre_check03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_pre_check03 pre_check試験03 異常系試験 (before_status: None, necessity: None)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・before_status = None
    ・necessity = None

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    before_status = None
    necessity = None

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status = mocker.Mock(return_value=before_status)
    test_mocker.necessity_check = mocker.Mock(return_value=necessity)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status", test_mocker.get_status)
    mocker.patch.object(process, "necessity_check", test_mocker.necessity_check)

    response_value = process.pre_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert test_mocker.get_status.called == True
    assert test_mocker.get_status.call_count == 1
    assert test_mocker.necessity_check.called == True
    assert test_mocker.necessity_check.call_count == 1
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_post_check01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_post_check01 post_check試験01 正常系試験 (after_status: Status.up, changed: ProcessStatus.change_ok)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・after_status = Status.up
    ・changed = ProcessStatus.change_ok

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    after_status = TargetStatus.up
    changed = ProcessStatus.change_ok

    command_response_value = []

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status = mocker.Mock(return_value=after_status)
    test_mocker.changed_check = mocker.Mock(return_value=changed)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status", test_mocker.get_status)
    mocker.patch.object(process, "changed_check", test_mocker.changed_check)

    response_value = process.post_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert test_mocker.get_status.called == True
    assert test_mocker.get_status.call_count == 1
    assert test_mocker.changed_check.called == True
    assert test_mocker.changed_check.call_count == 1
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_post_check02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_post_check02 post_check試験02 準正常系試験 (after_status: Status.up, changed: ProcessStatus.change_ng)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・after_status = Status.up
    ・changed = ProcessStatus.change_ng

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    after_status = TargetStatus.down
    changed = ProcessStatus.change_ng

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status = mocker.Mock(return_value=after_status)
    test_mocker.changed_check = mocker.Mock(return_value=changed)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status", test_mocker.get_status)
    mocker.patch.object(process, "changed_check", test_mocker.changed_check)

    response_value = process.post_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert test_mocker.get_status.called == True
    assert test_mocker.get_status.call_count == 1
    assert test_mocker.changed_check.called == True
    assert test_mocker.changed_check.call_count == 1
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_post_check03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_post_check03 post_check試験03 異常系試験 (after_status: None, changed: False)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・after_status = None
    ・changed = ProcessStatus.exception_ng

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    after_status = None
    changed = ProcessStatus.exception_ng

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status = mocker.Mock(return_value=after_status)
    test_mocker.changed_check = mocker.Mock(return_value=changed)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status", test_mocker.get_status)
    mocker.patch.object(process, "changed_check", test_mocker.changed_check)

    response_value = process.post_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert test_mocker.get_status.called == True
    assert test_mocker.get_status.call_count == 1
    assert test_mocker.changed_check.called == True
    assert test_mocker.changed_check.call_count == 1
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_change_status01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_change_status01 change_status試験01 正常系試験 (mode: Mode.up)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・before_status = Status.down
    ・get_status_word = "deregistered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    before_status = TargetStatus.down
    get_status_word = "deregistered"
    fill = [get_status_word, before_status]

    is_deregistered = True
    is_registered = True
    is_abort = None
    is_commit = True

    command_response_value = []

    expected_value = ProcessStatus.commit_ok

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.to_down = mocker.Mock(return_value=is_deregistered)
    test_mocker.to_up = mocker.Mock(return_value=is_registered)
    test_mocker.do_abort = mocker.Mock(return_value=is_abort)
    test_mocker.commit = mocker.Mock(return_value=is_commit)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    process.before_status = before_status

    mocker.patch.object(process, "to_down", test_mocker.to_down)
    mocker.patch.object(process, "to_up", test_mocker.to_up)
    mocker.patch.object(process, "do_abort", test_mocker.do_abort)
    mocker.patch.object(process, "commit", test_mocker.commit)
    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.change_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert test_mocker.to_down.called == False
    assert test_mocker.to_down.call_count == 0
    assert test_mocker.to_up.called == True
    assert test_mocker.to_up.call_count == 1
    assert test_mocker.do_abort.called == False
    assert test_mocker.do_abort.call_count == 0
    assert test_mocker.commit.called == True
    assert test_mocker.commit.call_count == 1
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_change_status02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_change_status02 change_status試験02 正常系試験 (mode: Mode.down)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・before_status = Status.up
    ・get_status_word = "registered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    before_status = TargetStatus.up
    get_status_word = "registered"
    fill = [get_status_word, before_status]

    is_deregistered = True
    is_registered = True
    is_abort = None
    is_commit = True

    command_response_value = []

    expected_value = ProcessStatus.commit_ok

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.to_down = mocker.Mock(return_value=is_deregistered)
    test_mocker.to_up = mocker.Mock(return_value=is_registered)
    test_mocker.do_abort = mocker.Mock(return_value=is_abort)
    test_mocker.commit = mocker.Mock(return_value=is_commit)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    process.before_status = before_status

    mocker.patch.object(process, "to_down", test_mocker.to_down)
    mocker.patch.object(process, "to_up", test_mocker.to_up)
    mocker.patch.object(process, "do_abort", test_mocker.do_abort)
    mocker.patch.object(process, "commit", test_mocker.commit)
    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.change_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert test_mocker.to_down.called == True
    assert test_mocker.to_down.call_count == 1
    assert test_mocker.to_up.called == False
    assert test_mocker.to_up.call_count == 0
    assert test_mocker.do_abort.called == False
    assert test_mocker.do_abort.call_count == 0
    assert test_mocker.commit.called == True
    assert test_mocker.commit.call_count == 1
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_change_status03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_change_status03 change_status試験03 準正常系試験 (mode: Mode.up, ステータス変更失敗)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・before_status = Status.down
    ・get_status_word = "deregistered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    before_status = TargetStatus.down
    get_status_word = "deregistered"
    fill = [get_status_word, before_status]

    is_deregistered = True
    is_registered = False
    is_abort = None
    is_commit = True

    command_response_value = []

    expected_value = ProcessStatus.change_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.to_down = mocker.Mock(return_value=is_deregistered)
    test_mocker.to_up = mocker.Mock(return_value=is_registered)
    test_mocker.do_abort = mocker.Mock(return_value=is_abort)
    test_mocker.commit = mocker.Mock(return_value=is_commit)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    process.before_status = before_status

    mocker.patch.object(process, "to_down", test_mocker.to_down)
    mocker.patch.object(process, "to_up", test_mocker.to_up)
    mocker.patch.object(process, "do_abort", test_mocker.do_abort)
    mocker.patch.object(process, "commit", test_mocker.commit)
    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.change_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert test_mocker.to_down.called == False
    assert test_mocker.to_down.call_count == 0
    assert test_mocker.to_up.called == True
    assert test_mocker.to_up.call_count == 1
    assert test_mocker.do_abort.called == True
    assert test_mocker.do_abort.call_count == 1
    assert test_mocker.commit.called == False
    assert test_mocker.commit.call_count == 0
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_change_status04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_change_status04 change_status試験04 準正常系試験 (mode: Mode.down, commit失敗)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・before_status = Status.up
    ・get_status_word = "registered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    before_status = TargetStatus.up
    get_status_word = "registered"
    fill = [get_status_word, before_status]

    is_deregistered = True
    is_registered = True
    is_abort = None
    is_commit = False

    command_response_value = []

    expected_value = ProcessStatus.commit_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.to_down = mocker.Mock(return_value=is_deregistered)
    test_mocker.to_up = mocker.Mock(return_value=is_registered)
    test_mocker.do_abort = mocker.Mock(return_value=is_abort)
    test_mocker.commit = mocker.Mock(return_value=is_commit)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    process.before_status = before_status

    mocker.patch.object(process, "to_down", test_mocker.to_down)
    mocker.patch.object(process, "to_up", test_mocker.to_up)
    mocker.patch.object(process, "do_abort", test_mocker.do_abort)
    mocker.patch.object(process, "commit", test_mocker.commit)
    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.change_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert test_mocker.to_down.called == True
    assert test_mocker.to_down.call_count == 1
    assert test_mocker.to_up.called == False
    assert test_mocker.to_up.call_count == 0
    assert test_mocker.do_abort.called == True
    assert test_mocker.do_abort.call_count == 1
    assert test_mocker.commit.called == True
    assert test_mocker.commit.call_count == 1
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_necessity_check01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_necessity_check01 necessity_check試験01 正常系試験 (mode: Mode.show, status: Status.up, 変更不要)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・status = Status.up
    ・get_status_word = "registered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    status = TargetStatus.up
    get_status_word = "registered"
    fill = [get_status_word, status]

    command_response_value = []

    expected_value = ProcessStatus.show_or_unknown

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.necessity_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_necessity_check02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_necessity_check02 necessity_check試験02 正常系試験 (mode: Mode.down, status: Status.down, 変更不要)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・status = Status.down
    ・get_status_word = "deregistered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    status = TargetStatus.down
    get_status_word = "deregistered"
    fill = [get_status_word, status]

    command_response_value = []

    expected_value = ProcessStatus.already_changed

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.necessity_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_necessity_check03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_necessity_check03 necessity_check試験03 正常系試験 (mode: Mode.up, status: Status.up, 変更不要)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・status = Status.up
    ・get_status_word = "registered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    status = TargetStatus.up
    get_status_word = "registered"
    fill = [get_status_word, status]

    command_response_value = []

    expected_value = ProcessStatus.already_changed

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.necessity_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_necessity_check04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_necessity_check04 necessity_check試験04 正常系試験 (mode: Mode.down, status: Status.up, 要変更)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・status = Status.up
    ・get_status_word = "registered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    status = TargetStatus.up
    get_status_word = "registered"
    fill = [get_status_word, status]

    command_response_value = []

    expected_value = ProcessStatus.need_to_change

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.necessity_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_necessity_check05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_necessity_check05 necessity_check試験05 正常系試験 (mode: Mode.up, status: Status.down, 要変更)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・status = Status.down
    ・get_status_word = "deregistered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    status = TargetStatus.down
    get_status_word = "deregistered"
    fill = [get_status_word, status]

    command_response_value = []

    expected_value = ProcessStatus.need_to_change

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.necessity_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_necessity_check06(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_necessity_check06 necessity_check試験06 異常系試験 (mode: Mode.up, status: Status.unknown, 異常)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・status = Status.unknown
    ・get_status_word = "unknown"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がNoneとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    status = TargetStatus.unknown
    get_status_word = "unknown"
    fill = [get_status_word, status]

    command_response_value = []

    expected_value = ProcessStatus.exception_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.necessity_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_changed_check01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_changed_check01 changed_check試験01 正常系試験 (mode: Mode.up, status: Status.up, 変更OK)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・status = Status.up
    ・get_status_word = "registered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    status = TargetStatus.up
    get_status_word = "registered"
    fill = [get_status_word, status]

    command_response_value = []

    expected_value = ProcessStatus.change_ok

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    response_value = process.changed_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_changed_check02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_changed_check02 changed_check試験02 正常系試験 (mode: Mode.down, status: Status.down, 変更OK)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・status = Status.down
    ・get_status_word = "deregistered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    status = TargetStatus.down
    get_status_word = "deregistered"
    fill = [get_status_word, status]

    command_response_value = []

    expected_value = ProcessStatus.change_ok

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    response_value = process.changed_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_changed_check03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_changed_check03 changed_check試験03 準正常系試験 (mode: Mode.up, status: Status.down, 変更失敗)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・status = Status.down
    ・get_status_word = "deregistered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    status = TargetStatus.down
    get_status_word = "deregistered"
    fill = [get_status_word, status]

    command_response_value = []

    expected_value = ProcessStatus.change_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:事後status変更失敗:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" MODE: {mode}\n",
        f" STATUS: {status}\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    response_value = process.changed_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_changed_check04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_changed_check04 changed_check試験03 準正常系試験 (mode: Mode.down, status: Status.up, 変更NG)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・status = Status.up
    ・get_status_word = "registered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    status = TargetStatus.up
    get_status_word = "registered"
    fill = [get_status_word, status]

    command_response_value = []

    expected_value = ProcessStatus.change_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    response_value = process.changed_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_changed_check05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_changed_check05 changed_check試験05 異常系試験 (mode: Mode.up, status: Status.unknown, 変更異常)

    試験条件
    ・alias = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・status = Status.unknown
    ・get_status_word = "unknown"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    alias = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    status = TargetStatus.unknown
    get_status_word = "unknown"
    fill = [get_status_word, status]

    command_response_value = []

    expected_value = ProcessStatus.exception_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = MockABC(alias, nf_name, mode, JOB_ID)
    process._AbcProcess__logger = logger

    response_value = process.changed_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
