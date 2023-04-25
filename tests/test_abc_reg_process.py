import pathlib
from typing import Any, List
import pytest
from pytest_mock import MockerFixture
from datetime import datetime

from xgnlog.Log import Level
from src.abc_process import AbcRegistrationProcess, ProcessStatus, Status

from src.xcap_common import Mode

JOB_ID = "T22AJ003"


def get_1st_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("1st_abc_reg_process.log")


def get_2nd_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("2nd_abc_reg_process.log")


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


class MockABC(AbcRegistrationProcess):
    def get_status(self) -> Status:
        pass

    def do_deregistered(self) -> bool:
        pass

    def do_registered(self) -> bool:
        pass

    def commit(self) -> bool:
        pass

    def do_abort(self) -> bool:
        pass

    def get_disp_status(self, status: Status) -> str:
        pass

    def run(self) -> ProcessStatus:
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
    status = Status.up
    value = Status.up.value

    expected_value = value

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    response_value = str(status)

    assert response_value == expected_value


def test_init01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_init01 __init__試験01 インスタンス生成

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show

    試験結果
    ・インスタンス生成が正常に終了すること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    process = MockABC(edns_host, nf_name, mode)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, MockABC)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_edns_host01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_edns_host01 edns_host試験01 edns_hostプロパティ取得

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show

    試験結果
    ・インスタンス生成が正常に終了すること
    ・edns_hostが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show

    expected_value = edns_host

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    process = MockABC(edns_host, nf_name, mode)

    response_value = process.edns_host

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcRegistrationProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_nf_name01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_nf_name01 nf_name試験01 nf_nameプロパティ取得

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show

    試験結果
    ・インスタンス生成が正常に終了すること
    ・nf_nameが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show

    expected_value = nf_name

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    process = MockABC(edns_host, nf_name, mode)

    response_value = process.nf_name

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcRegistrationProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_mode01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_mode01 mode試験01 modeプロパティ取得

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show

    試験結果
    ・インスタンス生成が正常に終了すること
    ・modeが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show

    expected_value = mode

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    process = MockABC(edns_host, nf_name, mode)

    response_value = process.mode

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcRegistrationProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_before_status01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_bfore_status01 before_status試験01 before_statusプロパティ取得

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・before_status = target.Status.down

    試験結果
    ・インスタンス生成が正常に終了すること
    ・before_statusが保存できること
    ・before_statusが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    before_status = Status.down

    expected_value = before_status

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    process = MockABC(edns_host, nf_name, mode)

    process.before_status = before_status
    response_value = process.before_status

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcRegistrationProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_after_status01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_after_status01 after_status試験01 after_statusプロパティ取得

    試験条件
    ・edns_host = "b1-CPA_East-Act"
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
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    after_status = Status.down

    expected_value = after_status

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    process = MockABC(edns_host, nf_name, mode)

    process.after_status = after_status
    response_value = process.after_status

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcRegistrationProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_is_need_to_change01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_is_need_to_change01 is_need_to_change試験01 is_need_to_changeプロパティ取得

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・is_need_to_change = true

    試験結果
    ・インスタンス生成が正常に終了すること
    ・is_need_to_changeが保存できること
    ・is_need_to_changeが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    is_need_to_change = True

    expected_value = is_need_to_change

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    process = MockABC(edns_host, nf_name, mode)

    process.is_need_to_change = is_need_to_change
    response_value = process.is_need_to_change

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcRegistrationProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_is_changed01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_is_changed01 is_changed試験01 is_changedプロパティ取得

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・is_changed = True

    試験結果
    ・インスタンス生成が正常に終了すること
    ・is_changedが保存できること
    ・is_changedが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    is_changed = True

    expected_value = is_changed

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    process = MockABC(edns_host, nf_name, mode)

    process.is_changed = is_changed
    response_value = process.is_changed

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, AbcRegistrationProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_pre_check01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_pre_check01 pre_check試験01 正常系試験 (before_status: Status.down, is_need_to_change: True)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・before_status = Status.down
    ・is_need_to_change = True

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    before_status = Status.down
    is_need_to_change = True

    command_response_value = []

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00301", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00302", [nf_name, f"pre_check: {expected_value}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status = mocker.Mock(return_value=before_status)
    test_mocker.check_before_status = mocker.Mock(return_value=is_need_to_change)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_status", test_mocker.get_status)
    mocker.patch.object(process, "check_before_status", test_mocker.check_before_status)

    response_value = process.pre_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.get_status.called == True
    assert test_mocker.get_status.call_count == 1
    assert test_mocker.check_before_status.called == True
    assert test_mocker.check_before_status.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_pre_check02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_pre_check02 pre_check試験02 正常系試験 (before_status: Status.down, is_need_to_change: False)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・before_status = Status.down
    ・is_need_to_change = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    before_status = Status.down
    is_need_to_change = False

    command_response_value = []

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00301", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00302", [nf_name, f"pre_check: {expected_value}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status = mocker.Mock(return_value=before_status)
    test_mocker.check_before_status = mocker.Mock(return_value=is_need_to_change)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_status", test_mocker.get_status)
    mocker.patch.object(process, "check_before_status", test_mocker.check_before_status)

    response_value = process.pre_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.get_status.called == True
    assert test_mocker.get_status.call_count == 1
    assert test_mocker.check_before_status.called == True
    assert test_mocker.check_before_status.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_pre_check03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_pre_check03 pre_check試験03 異常系試験 (before_status: None, is_need_to_change: None)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・before_status = None
    ・is_need_to_change = None

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    before_status = None
    is_need_to_change = None

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00301", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00302", [nf_name, f"pre_check: {expected_value}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status = mocker.Mock(return_value=before_status)
    test_mocker.check_before_status = mocker.Mock(return_value=is_need_to_change)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_status", test_mocker.get_status)
    mocker.patch.object(process, "check_before_status", test_mocker.check_before_status)

    response_value = process.pre_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.get_status.called == True
    assert test_mocker.get_status.call_count == 1
    assert test_mocker.check_before_status.called == True
    assert test_mocker.check_before_status.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_post_check01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_post_check01 post_check試験01 正常系試験 (after_status: Status.up, is_changed: True)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・after_status = Status.up
    ・is_changed = True

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    after_status = Status.up
    is_changed = True

    command_response_value = []

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00303", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00304", [nf_name, f"post_check: {expected_value}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status = mocker.Mock(return_value=after_status)
    test_mocker.check_after_status = mocker.Mock(return_value=is_changed)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_status", test_mocker.get_status)
    mocker.patch.object(process, "check_after_status", test_mocker.check_after_status)

    response_value = process.post_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.get_status.called == True
    assert test_mocker.get_status.call_count == 1
    assert test_mocker.check_after_status.called == True
    assert test_mocker.check_after_status.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_post_check02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_post_check02 post_check試験02 準正常系試験 (after_status: Status.down, is_changed: False)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・after_status = Status.down
    ・is_changed = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    after_status = Status.down
    is_changed = False

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00303", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00304", [nf_name, f"post_check: {expected_value}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status = mocker.Mock(return_value=after_status)
    test_mocker.check_after_status = mocker.Mock(return_value=is_changed)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_status", test_mocker.get_status)
    mocker.patch.object(process, "check_after_status", test_mocker.check_after_status)

    response_value = process.post_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.get_status.called == True
    assert test_mocker.get_status.call_count == 1
    assert test_mocker.check_after_status.called == True
    assert test_mocker.check_after_status.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_post_check03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_post_check03 post_check試験03 異常系試験 (after_status: None, is_changed: False)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・after_status = None
    ・is_changed = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    after_status = None
    is_changed = False

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00303", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00304", [nf_name, f"post_check: {expected_value}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_status = mocker.Mock(return_value=after_status)
    test_mocker.check_after_status = mocker.Mock(return_value=is_changed)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_status", test_mocker.get_status)
    mocker.patch.object(process, "check_after_status", test_mocker.check_after_status)

    response_value = process.post_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.get_status.called == True
    assert test_mocker.get_status.call_count == 1
    assert test_mocker.check_after_status.called == True
    assert test_mocker.check_after_status.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_change_status01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_change_status01 change_status試験01 正常系試験 (mode: Mode.up)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・before_status = Status.down
    ・disp_status = "deregistered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    before_status = Status.down
    disp_status = "deregistered"
    fill = [disp_status, before_status]

    is_deregistered = True
    is_registered = True
    is_abort = None
    is_commit = True

    command_response_value = []

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00305", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00306", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.do_deregistered = mocker.Mock(return_value=is_deregistered)
    test_mocker.do_registered = mocker.Mock(return_value=is_registered)
    test_mocker.do_abort = mocker.Mock(return_value=is_abort)
    test_mocker.commit = mocker.Mock(return_value=is_commit)
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    process.before_status = before_status

    mocker.patch.object(process, "do_deregistered", test_mocker.do_deregistered)
    mocker.patch.object(process, "do_registered", test_mocker.do_registered)
    mocker.patch.object(process, "do_abort", test_mocker.do_abort)
    mocker.patch.object(process, "commit", test_mocker.commit)
    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.change_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.do_deregistered.called == False
    assert test_mocker.do_deregistered.call_count == 0
    assert test_mocker.do_registered.called == True
    assert test_mocker.do_registered.call_count == 1
    assert test_mocker.do_abort.called == False
    assert test_mocker.do_abort.call_count == 0
    assert test_mocker.commit.called == True
    assert test_mocker.commit.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_change_status02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_change_status02 change_status試験02 正常系試験 (mode: Mode.down)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・before_status = Status.up
    ・disp_status = "registered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    before_status = Status.up
    disp_status = "registered"
    fill = [disp_status, before_status]

    is_deregistered = True
    is_registered = True
    is_abort = None
    is_commit = True

    command_response_value = []

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00305", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00306", nf_name)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.do_deregistered = mocker.Mock(return_value=is_deregistered)
    test_mocker.do_registered = mocker.Mock(return_value=is_registered)
    test_mocker.do_abort = mocker.Mock(return_value=is_abort)
    test_mocker.commit = mocker.Mock(return_value=is_commit)
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    process.before_status = before_status

    mocker.patch.object(process, "do_deregistered", test_mocker.do_deregistered)
    mocker.patch.object(process, "do_registered", test_mocker.do_registered)
    mocker.patch.object(process, "do_abort", test_mocker.do_abort)
    mocker.patch.object(process, "commit", test_mocker.commit)
    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.change_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.do_deregistered.called == True
    assert test_mocker.do_deregistered.call_count == 1
    assert test_mocker.do_registered.called == False
    assert test_mocker.do_registered.call_count == 0
    assert test_mocker.do_abort.called == False
    assert test_mocker.do_abort.call_count == 0
    assert test_mocker.commit.called == True
    assert test_mocker.commit.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_change_status03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_change_status03 change_status試験03 準正常系試験 (mode: Mode.up, ステータス変更失敗)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・before_status = Status.down
    ・disp_status = "deregistered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    before_status = Status.down
    disp_status = "deregistered"
    fill = [disp_status, before_status]

    is_deregistered = True
    is_registered = False
    is_abort = None
    is_commit = True

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):status change was failed. abort has done. current status is {0}. [ {1} ]\n".format(*fill, mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00305", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00301", [nf_name, mode])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.do_deregistered = mocker.Mock(return_value=is_deregistered)
    test_mocker.do_registered = mocker.Mock(return_value=is_registered)
    test_mocker.do_abort = mocker.Mock(return_value=is_abort)
    test_mocker.commit = mocker.Mock(return_value=is_commit)
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    process.before_status = before_status

    mocker.patch.object(process, "do_deregistered", test_mocker.do_deregistered)
    mocker.patch.object(process, "do_registered", test_mocker.do_registered)
    mocker.patch.object(process, "do_abort", test_mocker.do_abort)
    mocker.patch.object(process, "commit", test_mocker.commit)
    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.change_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.do_deregistered.called == False
    assert test_mocker.do_deregistered.call_count == 0
    assert test_mocker.do_registered.called == True
    assert test_mocker.do_registered.call_count == 1
    assert test_mocker.do_abort.called == True
    assert test_mocker.do_abort.call_count == 1
    assert test_mocker.commit.called == False
    assert test_mocker.commit.call_count == 0
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_change_status04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_change_status04 change_status試験04 準正常系試験 (mode: Mode.down, commit失敗)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・before_status = Status.up
    ・disp_status = "registered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    before_status = Status.up
    disp_status = "registered"
    fill = [disp_status, before_status]

    is_deregistered = True
    is_registered = True
    is_abort = None
    is_commit = False

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):commit was failed. abort has done.\n".format(mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00305", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00302", [nf_name, mode])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.do_deregistered = mocker.Mock(return_value=is_deregistered)
    test_mocker.do_registered = mocker.Mock(return_value=is_registered)
    test_mocker.do_abort = mocker.Mock(return_value=is_abort)
    test_mocker.commit = mocker.Mock(return_value=is_commit)
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    process.before_status = before_status

    mocker.patch.object(process, "do_deregistered", test_mocker.do_deregistered)
    mocker.patch.object(process, "do_registered", test_mocker.do_registered)
    mocker.patch.object(process, "do_abort", test_mocker.do_abort)
    mocker.patch.object(process, "commit", test_mocker.commit)
    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.change_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.do_deregistered.called == True
    assert test_mocker.do_deregistered.call_count == 1
    assert test_mocker.do_registered.called == False
    assert test_mocker.do_registered.call_count == 0
    assert test_mocker.do_abort.called == True
    assert test_mocker.do_abort.call_count == 1
    assert test_mocker.commit.called == True
    assert test_mocker.commit.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_before_status01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_before_status01 check_before_status試験01 正常系試験 (mode: Mode.show, status: Status.up, 変更不要)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・status = Status.up
    ・disp_status = "registered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    status = Status.up
    disp_status = "registered"
    fill = [disp_status, status]

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[INFO]:{mode}:{time}:{edns_host}({nf_name}):nf registration current status is {0}. [ {1} ]\n".format(*fill, mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00307", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00311", [nf_name, mode, status]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00308", [nf_name, f"need_to_change: {expected_value}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.check_before_status(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_before_status02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_before_status02 check_before_status試験02 正常系試験 (mode: Mode.down, status: Status.down, 変更不要)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・status = Status.down
    ・disp_status = "deregistered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    status = Status.down
    disp_status = "deregistered"
    fill = [disp_status, status]

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[SUCCESS]:{mode}:{time}:{edns_host}({nf_name}):nf registration current status is already {0}. [ {1} ]\n".format(*fill, mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00307", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00311", [nf_name, mode, status]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00308", [nf_name, f"need_to_change: {expected_value}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.check_before_status(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_before_status03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_before_status03 check_before_status試験03 正常系試験 (mode: Mode.up, status: Status.up, 変更不要)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・status = Status.up
    ・disp_status = "registered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    status = Status.up
    disp_status = "registered"
    fill = [disp_status, status]

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[SUCCESS]:{mode}:{time}:{edns_host}({nf_name}):nf registration current status is already {0}. [ {1} ]\n".format(*fill, mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00307", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00311", [nf_name, mode, status]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00308", [nf_name, f"need_to_change: {expected_value}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.check_before_status(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_before_status04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_before_status04 check_before_status試験04 正常系試験 (mode: Mode.down, status: Status.up, 要変更)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・status = Status.up
    ・disp_status = "registered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    status = Status.up
    disp_status = "registered"
    fill = [disp_status, status]

    command_response_value = []

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[INFO]:{mode}:{time}:{edns_host}({nf_name}):nf registration current status is {0}. [ {1} ]\n".format(*fill, mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00307", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00312", [nf_name, mode, status]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00308", [nf_name, f"need_to_change: {expected_value}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.check_before_status(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_before_status05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_before_status05 check_before_status試験05 正常系試験 (mode: Mode.up, status: Status.down, 要変更)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・status = Status.down
    ・disp_status = "deregistered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    status = Status.down
    disp_status = "deregistered"
    fill = [disp_status, status]

    command_response_value = []

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[INFO]:{mode}:{time}:{edns_host}({nf_name}):nf registration current status is {0}. [ {1} ]\n".format(*fill, mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00307", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00312", [nf_name, mode, status]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00308", [nf_name, f"need_to_change: {expected_value}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.check_before_status(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_before_status06(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_before_status06 check_before_status試験06 異常系試験 (mode: Mode.up, status: Status.unknown, 異常)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・status = Status.unknown
    ・disp_status = "unknown"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がNoneとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    status = Status.unknown
    disp_status = "unknown"
    fill = [disp_status, status]

    command_response_value = []

    expected_value = None

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):nf registration currentry status couldn't get or mismatch. [ UNKNOWN ]\n".format(mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00307", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00303", [nf_name, mode, status]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00308", [nf_name, f"need_to_change: {expected_value}"])
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:事前registration status取得失敗:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" MODE: {mode}\n",
        f" STATUS: {status}\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.check_before_status(status)

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
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_check_after_status01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_after_status01 check_after_status試験01 正常系試験 (mode: Mode.up, status: Status.up, 変更OK)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・status = Status.up
    ・disp_status = "registered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    status = Status.up
    disp_status = "registered"
    fill = [disp_status, status]

    command_response_value = []

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[SUCCESS]:{mode}:{time}:{edns_host}({nf_name}):nf registration current status is {0}. [ {1} ]\n".format(*fill, mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00309", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00313", [nf_name, mode, status]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00310", [nf_name, f"changed: {expected_value}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.check_after_status(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_after_status02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_after_status02 check_after_status試験02 正常系試験 (mode: Mode.down, status: Status.down, 変更OK)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・status = Status.down
    ・disp_status = "deregistered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    status = Status.down
    disp_status = "deregistered"
    fill = [disp_status, status]

    command_response_value = []

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[SUCCESS]:{mode}:{time}:{edns_host}({nf_name}):nf registration current status is {0}. [ {1} ]\n".format(*fill, mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00309", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00313", [nf_name, mode, status]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00310", [nf_name, f"changed: {expected_value}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.check_after_status(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_after_status03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_after_status03 check_after_status試験03 準正常系試験 (mode: Mode.up, status: Status.down, 変更失敗)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・status = Status.down
    ・disp_status = "deregistered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    status = Status.down
    disp_status = "deregistered"
    fill = [disp_status, status]

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):nf registration status couldn't change... still {0}. [ {1} ]\n".format(*fill, mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00309", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00304", [nf_name, mode, status]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00310", [nf_name, f"changed: {expected_value}"])
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:事後registration status変更失敗:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" MODE: {mode}\n",
        f" STATUS: {status}\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.check_after_status(status)

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
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_check_after_status04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_after_status04 check_after_status試験03 準正常系試験 (mode: Mode.down, status: Status.up, 変更OK)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・status = Status.up
    ・disp_status = "registered"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    status = Status.up
    disp_status = "registered"
    fill = [disp_status, status]

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):nf registration status couldn't change... still {0}. [ {1} ]\n".format(*fill, mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00309", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00304", [nf_name, mode, status]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00310", [nf_name, f"changed: {expected_value}"])
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:事後registration status変更失敗:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" MODE: {mode}\n",
        f" STATUS: {status}\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.check_after_status(status)

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
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_check_after_status05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_after_status05 check_after_status試験05 異常系試験 (mode: Mode.up, status: Status.unknown, 変更異常)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・status = Status.unknown
    ・disp_status = "unknown"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    status = Status.unknown
    disp_status = "unknown"
    fill = [disp_status, status]

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):nf registration currentry status couldn't get or mismatch. [ UNKNOWN ]\n".format(mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00309", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00303", [nf_name, mode, status]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00310", [nf_name, f"changed: {expected_value}"])
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:事後registration status取得失敗:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" MODE: {mode}\n",
        f" STATUS: {status}\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.get_disp_status = mocker.Mock(return_value=disp_status)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = MockABC(edns_host, nf_name, mode)

    mocker.patch.object(process, "get_disp_status", test_mocker.get_disp_status)

    response_value = process.check_after_status(status)

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
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd
