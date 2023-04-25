import pathlib
from typing import Any, List
import pytest
from pytest_mock import MockerFixture
from datetime import datetime

from xgnlog.Log import Level
from src.abc_process import ProcessStatus, Status
from src.eri_connection import SocketTimeoutException
from src.eri_smfvo_xcap_process import EriSmfvoXCAPProcess

from src.xcap_common import Mode

JOB_ID = "T22AJ003"


def get_1st_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("1st_eri_smf_reg_process.log")


def get_2nd_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("2nd_eri_smf_reg_process.log")


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


class TestClient():
    def __init__(self, name: str):
        pass


class TestStubClient():
    def __init__(self, mode: Mode, name: str):
        pass


def test_get_reg_dereg_pattern01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_reg_dereg_pattern01 get_reg_dereg_pattern試験01 正常系試験 (Status:down)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False
    ・status = Status.down

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False
    status = Status.down

    expected_value = "nf-status deregistered"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.out_message = mocker.Mock(return_value=True)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._EriSmfRegistrationProcess__client = test_mocker

    response_value = process.get_reg_dereg_pattern(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_get_reg_dereg_pattern02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_reg_dereg_pattern02 get_reg_dereg_pattern試験02 正常系試験 (Status:up)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False
    ・status = Status.up

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False
    status = Status.up

    expected_value = "nf-status registered"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.out_message = mocker.Mock(return_value=True)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._EriSmfRegistrationProcess__client = test_mocker

    response_value = process.get_reg_dereg_pattern(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_get_reg_dereg_pattern03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_reg_dereg_pattern03 get_reg_dereg_pattern試験03 異常系試験 (Status:unknown)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False
    ・status = Status.down

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False
    status = Status.unknown

    expected_value = None

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.out_message = mocker.Mock(return_value=True)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._EriSmfRegistrationProcess__client = test_mocker

    response_value = process.get_reg_dereg_pattern(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_get_command01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_command01 get_command試験01 正常系試験 (Mode:down)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False

    expected_value = "epg pgw sbi smf-service nf-status deregistered"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.out_message = mocker.Mock(return_value=True)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._EriSmfRegistrationProcess__client = test_mocker

    response_value = process.get_command(mode)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_get_command02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_command02 get_command試験02 正常系試験 (Mode:up)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    stub = False

    expected_value = "epg pgw sbi smf-service nf-status registered"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.out_message = mocker.Mock(return_value=True)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._EriSmfRegistrationProcess__client = test_mocker

    response_value = process.get_command(mode)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_get_command03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_command03 get_command試験03 正常系試験 (Mode:show)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False

    expected_value = "show running-config epg pgw sbi smf-service nf-status"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.out_message = mocker.Mock(return_value=True)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._EriSmfRegistrationProcess__client = test_mocker

    response_value = process.get_command(mode)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_get_command04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_command04 get_command試験04 異常系試験 (Mode:None)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = None
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = None
    stub = False

    expected_value = None

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.out_message = mocker.Mock(return_value=True)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._EriSmfRegistrationProcess__client = test_mocker

    response_value = process.get_command(mode)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_get_disp_status01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_disp_status01 get_disp_status試験01 正常系試験 (Status:down)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・stub = False
    ・status = Status.down

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False
    status = Status.down

    expected_value = "deregistered"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.out_message = mocker.Mock(return_value=True)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._EriSmfRegistrationProcess__client = test_mocker

    response_value = process.get_disp_status(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_get_disp_status02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_disp_status02 get_disp_status試験02 正常系試験 (Status:up)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・stub = False
    ・status = Status.up

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    stub = False
    status = Status.up

    expected_value = "registered"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.out_message = mocker.Mock(return_value=True)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._EriSmfRegistrationProcess__client = test_mocker

    response_value = process.get_disp_status(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_get_disp_status03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_disp_status03 get_disp_status試験03 異常系試験 (Status:unknown)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・stub = False
    ・status = Status.unknown

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False
    status = Status.unknown

    expected_value = "unknown"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.out_message = mocker.Mock(return_value=True)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._EriSmfRegistrationProcess__client = test_mocker

    response_value = process.get_disp_status(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_get_status01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_status01 get_status試験01 正常系試験 (registered)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・stub = False
    ・status = Status.up

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がStatus.upとなること
    ・get_reg_dereg_patternが2回呼ばれること
    ・get_commandが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False
    status = Status.up

    reg_dereg_pattern = [
        "nf-status registered",
        "nf-status deregistered"
    ]

    send_command = [
        "show running-config epg pgw sbi smf-service nf-status"
    ]

    command_response_value = [
        "epg pgw sbi smf-service nf-status registered\n".encode("utf-8")  # show run
    ]

    expected_value = Status.up

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00324", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", send_command[0]),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[0].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00325", [nf_name, status])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.get_reg_dereg_pattern = mocker.Mock(side_effect=reg_dereg_pattern)
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.command = mocker.Mock(side_effect=[*command_response_value])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    mocker.patch.object(process, "get_reg_dereg_pattern", test_mocker.get_reg_dereg_pattern)
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.get_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.get_reg_dereg_pattern.called == True
    assert test_mocker.get_reg_dereg_pattern.call_count == 2
    assert test_mocker.get_command.called == True
    assert test_mocker.get_command.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_status02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_status02 get_status試験02 正常系試験 (deregistered)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・stub = False
    ・status = Status.down

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がStatus.downとなること
    ・get_reg_dereg_patternが2回呼ばれること
    ・get_commandが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    stub = False
    status = Status.down

    reg_dereg_pattern = [
        "nf-status registered",
        "nf-status deregistered"
    ]

    send_command = [
        "show running-config epg pgw sbi smf-service nf-status"
    ]

    command_response_value = [
        "epg pgw sbi smf-service nf-status deregistered\n".encode("utf-8")  # show run
    ]

    expected_value = Status.down

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00324", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", send_command[0]),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[0].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00325", [nf_name, status])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.get_reg_dereg_pattern = mocker.Mock(side_effect=reg_dereg_pattern)
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.command = mocker.Mock(side_effect=[*command_response_value])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    mocker.patch.object(process, "get_reg_dereg_pattern", test_mocker.get_reg_dereg_pattern)
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.get_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.get_reg_dereg_pattern.called == True
    assert test_mocker.get_reg_dereg_pattern.call_count == 2
    assert test_mocker.get_command.called == True
    assert test_mocker.get_command.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_status03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_status03 get_status試験03 準正常系試験 (unknown)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・stub = False
    ・status = Status.unknown

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がStatus.unknownとなること
    ・get_reg_dereg_patternが2回呼ばれること
    ・get_commandが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    stub = False
    status = Status.unknown

    reg_dereg_pattern = [
        "nf-status registered",
        "nf-status deregistered"
    ]

    send_command = [
        "show running-config epg pgw sbi smf-service nf-status"
    ]

    command_response_value = [
        "epg pgw sbi smf-service nf-status undiscoverable\n".encode("utf-8")  # show run
    ]

    expected_value = Status.unknown

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00324", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", send_command[0]),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[0].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00325", [nf_name, status])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.get_reg_dereg_pattern = mocker.Mock(side_effect=reg_dereg_pattern)
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.command = mocker.Mock(side_effect=[*command_response_value])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    mocker.patch.object(process, "get_reg_dereg_pattern", test_mocker.get_reg_dereg_pattern)
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.get_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.get_reg_dereg_pattern.called == True
    assert test_mocker.get_reg_dereg_pattern.call_count == 2
    assert test_mocker.get_command.called == True
    assert test_mocker.get_command.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_status04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_status04 get_status試験04 異常系試験 (SocketTimeoutException発生)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・stub = False
    ・SocketTimeoutException発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がNoneとなること
    ・get_reg_dereg_patternが2回呼ばれること
    ・get_commandが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    stub = False
    status = Status.unknown

    reg_dereg_pattern = [
        "nf-status registered",
        "nf-status deregistered"
    ]

    send_command = [
        "show running-config epg pgw sbi smf-service nf-status"
    ]

    command_response_value = []

    expected_value = None

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):ssh connection timeout was happened. [ UNKNOWN ]\n".format(mode=mode, time=logtime_str, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00324", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", send_command[0]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00307", nf_name)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:registration status取得失敗:\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: {send_command[0]}\n",
        f" Trace: SocketTimeoutException Test SocketTimeoutException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.get_reg_dereg_pattern = mocker.Mock(side_effect=reg_dereg_pattern)
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.command = mocker.Mock(side_effect=[SocketTimeoutException("Test SocketTimeoutException")])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    mocker.patch.object(process, "get_reg_dereg_pattern", test_mocker.get_reg_dereg_pattern)
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.get_status()

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
    assert test_mocker.get_reg_dereg_pattern.called == True
    assert test_mocker.get_reg_dereg_pattern.call_count == 2
    assert test_mocker.get_command.called == True
    assert test_mocker.get_command.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_do_registered01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_do_registered01 do_registered試験01 正常系試験 (OK)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・get_commandが1回呼ばれること
    ・client.enter_config_modeが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    stub = False

    send_command = [
        "epg pgw sbi smf-service nf-status registered"
    ]

    command_response_value = [
        "\n".encode("utf-8")  # registered
    ]

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00328", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "config"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", send_command[0]),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[0].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00329", [nf_name, mode, True])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=command_response_value)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.do_registered()

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
    assert test_mocker.get_command.called == True
    assert test_mocker.get_command.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_do_registered02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_do_registered02 do_registered試験02 異常系試験 (SocketTimeoutException発生)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・get_commandが1回呼ばれること
    ・client.enter_config_modeが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    stub = False

    send_command = [
        "epg pgw sbi smf-service nf-status registered"
    ]

    command_response_value = [
        "\n".encode("utf-8")  # registered
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):ssh connection timeout was happened. [ UNKNOWN ]\n".format(mode=mode, time=logtime_str, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00328", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "config"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", send_command[0]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00308", [nf_name, mode])
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:registration status to registerd変更異常(timeout):\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: {send_command[0]}\n",
        f" Trace: SocketTimeoutException Test SocketTimeoutException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[SocketTimeoutException("Test SocketTimeoutException")])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.do_registered()

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
    assert test_mocker.get_command.called == True
    assert test_mocker.get_command.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_do_registered03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_do_registered03 do_registered試験03 異常系試験 (その他Exception発生)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・get_commandが1回呼ばれること
    ・client.enter_config_modeが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    stub = False

    send_command = [
        "epg pgw sbi smf-service nf-status registered"
    ]

    command_response_value = [
        "\n".encode("utf-8")  # registered
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00328", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "config"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", send_command[0]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00308", [nf_name, mode])
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:registration status to registerd変更異常(other):\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: {send_command[0]}\n",
        f" Trace: Exception Test Exception\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[Exception("Test Exception")])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.do_registered()

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
    assert test_mocker.get_command.called == True
    assert test_mocker.get_command.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_do_deregistered01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_do_deregistered01 do_deregistered試験01 正常系試験 (OK)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・get_commandが1回呼ばれること
    ・client.enter_config_modeが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False

    send_command = [
        "epg pgw sbi smf-service nf-status deregistered"
    ]

    command_response_value = [
        "\n".encode("utf-8")  # deregistered
    ]

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00326", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "config"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", send_command[0]),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", command_response_value[0].decode("utf-8")).splitlines(True),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00327", [nf_name, mode, True])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=command_response_value)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.do_deregistered()

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
    assert test_mocker.get_command.called == True
    assert test_mocker.get_command.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_do_deregistered02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_do_deregistered02 do_deregistered試験02 異常系試験 (SocketTimeoutException発生)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・get_commandが1回呼ばれること
    ・client.enter_config_modeが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False

    send_command = [
        "epg pgw sbi smf-service nf-status deregistered"
    ]

    command_response_value = [
        "\n".encode("utf-8")  # deregistered
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):ssh connection timeout was happened. [ UNKNOWN ]\n".format(mode=mode, time=logtime_str, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00326", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "config"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", send_command[0]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00308", [nf_name, mode])
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:registration status to deregisterd変更異常(timeout):\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: {send_command[0]}\n",
        f" Trace: SocketTimeoutException Test SocketTimeoutException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[SocketTimeoutException("Test SocketTimeoutException")])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.do_deregistered()

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
    assert test_mocker.get_command.called == True
    assert test_mocker.get_command.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_do_deregistered03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_do_deregistered03 do_deregistered試験03 異常系試験 (その他Exception発生)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・get_commandが1回呼ばれること
    ・client.enter_config_modeが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False

    send_command = [
        "epg pgw sbi smf-service nf-status deregistered"
    ]

    command_response_value = [
        "\n".encode("utf-8")  # deregistered
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00326", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", "config"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00323", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00322", send_command[0]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00308", [nf_name, mode])
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:registration status to deregisterd変更異常(other):\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: {send_command[0]}\n",
        f" Trace: Exception Test Exception\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[Exception("Test Exception")])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.do_deregistered()

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
    assert test_mocker.get_command.called == True
    assert test_mocker.get_command.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_run01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_run01 run試験01 正常系試験 (OK, mode:Mode.up)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がProcessStatus.post_check_okとなること
    ・open_clientが1回呼ばれること
    ・pre_checkが1回呼ばれること
    ・change_statusが1回呼ばれること
    ・post_checkが1回呼ばれること
    ・close_clientが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    stub = False
    status = ProcessStatus.post_check_ok

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.post_check_ok

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00330", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00331", [nf_name, f"process status: {status}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=True)
    test_mocker.pre_check = mocker.Mock(return_value=True)
    test_mocker.change_status = mocker.Mock(return_value=True)
    test_mocker.post_check = mocker.Mock(return_value=True)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    process.is_need_to_change = True
    mocker.patch("time.sleep", test_mocker.sleep)
    mocker.patch.object(process, "open_client", test_mocker.open_client)
    mocker.patch.object(process, "pre_check", test_mocker.pre_check)
    mocker.patch.object(process, "change_status", test_mocker.change_status)
    mocker.patch.object(process, "post_check", test_mocker.post_check)
    mocker.patch.object(process, "close_client", test_mocker.close_client)

    response_value = process.run()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.open_client.called == True
    assert test_mocker.open_client.call_count == 1
    assert test_mocker.pre_check.called == True
    assert test_mocker.pre_check.call_count == 1
    assert test_mocker.change_status.called == True
    assert test_mocker.change_status.call_count == 1
    assert test_mocker.post_check.called == True
    assert test_mocker.post_check.call_count == 1
    assert test_mocker.close_client.called == True
    assert test_mocker.close_client.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_run02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_run02 run試験02 正常系試験 (OK, mode:Mode.down)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.down
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がProcessStatus.post_check_okとなること
    ・open_clientが1回呼ばれること
    ・pre_checkが1回呼ばれること
    ・change_statusが1回呼ばれること
    ・post_checkが1回呼ばれること
    ・close_clientが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.down
    stub = False
    status = ProcessStatus.post_check_ok

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.post_check_ok

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00330", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00331", [nf_name, f"process status: {status}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=True)
    test_mocker.pre_check = mocker.Mock(return_value=True)
    test_mocker.change_status = mocker.Mock(return_value=True)
    test_mocker.post_check = mocker.Mock(return_value=True)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    process.is_need_to_change = True
    mocker.patch("time.sleep", test_mocker.sleep)
    mocker.patch.object(process, "open_client", test_mocker.open_client)
    mocker.patch.object(process, "pre_check", test_mocker.pre_check)
    mocker.patch.object(process, "change_status", test_mocker.change_status)
    mocker.patch.object(process, "post_check", test_mocker.post_check)
    mocker.patch.object(process, "close_client", test_mocker.close_client)

    response_value = process.run()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.open_client.called == True
    assert test_mocker.open_client.call_count == 1
    assert test_mocker.pre_check.called == True
    assert test_mocker.pre_check.call_count == 1
    assert test_mocker.change_status.called == True
    assert test_mocker.change_status.call_count == 1
    assert test_mocker.post_check.called == True
    assert test_mocker.post_check.call_count == 1
    assert test_mocker.close_client.called == True
    assert test_mocker.close_client.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_run03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_run03 run試験03 正常系試験 (OK, mode:Mode.show)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がProcessStatus.need_not_to_changeとなること
    ・open_clientが1回呼ばれること
    ・pre_checkが1回呼ばれること
    ・change_statusが0回呼ばれること
    ・post_checkが0回呼ばれること
    ・close_clientが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False
    status = ProcessStatus.need_not_to_change

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.need_not_to_change

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00330", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00331", [nf_name, f"process status: {status}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=True)
    test_mocker.pre_check = mocker.Mock(return_value=True)
    test_mocker.change_status = mocker.Mock(return_value=False)
    test_mocker.post_check = mocker.Mock(return_value=False)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    process.is_need_to_change = False
    mocker.patch("time.sleep", test_mocker.sleep)
    mocker.patch.object(process, "open_client", test_mocker.open_client)
    mocker.patch.object(process, "pre_check", test_mocker.pre_check)
    mocker.patch.object(process, "change_status", test_mocker.change_status)
    mocker.patch.object(process, "post_check", test_mocker.post_check)
    mocker.patch.object(process, "close_client", test_mocker.close_client)

    response_value = process.run()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.open_client.called == True
    assert test_mocker.open_client.call_count == 1
    assert test_mocker.pre_check.called == True
    assert test_mocker.pre_check.call_count == 1
    assert test_mocker.change_status.called == False
    assert test_mocker.change_status.call_count == 0
    assert test_mocker.post_check.called == False
    assert test_mocker.post_check.call_count == 0
    assert test_mocker.close_client.called == True
    assert test_mocker.close_client.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_run04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_run04 run試験04 異常系試験 (OK, mode:Mode.show, SSH接続異常)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がProcessStatus.ssh_ngとなること
    ・open_clientが1回呼ばれること
    ・pre_checkが0回呼ばれること
    ・change_statusが0回呼ばれること
    ・post_checkが0回呼ばれること
    ・close_clientが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False
    status = ProcessStatus.ssh_ng

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.ssh_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00330", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00331", [nf_name, f"process status: {status}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=False)
    test_mocker.pre_check = mocker.Mock(return_value=False)
    test_mocker.change_status = mocker.Mock(return_value=False)
    test_mocker.post_check = mocker.Mock(return_value=False)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    mocker.patch("time.sleep", test_mocker.sleep)
    mocker.patch.object(process, "open_client", test_mocker.open_client)
    mocker.patch.object(process, "pre_check", test_mocker.pre_check)
    mocker.patch.object(process, "change_status", test_mocker.change_status)
    mocker.patch.object(process, "post_check", test_mocker.post_check)
    mocker.patch.object(process, "close_client", test_mocker.close_client)

    response_value = process.run()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.open_client.called == True
    assert test_mocker.open_client.call_count == 1
    assert test_mocker.pre_check.called == False
    assert test_mocker.pre_check.call_count == 0
    assert test_mocker.change_status.called == False
    assert test_mocker.change_status.call_count == 0
    assert test_mocker.post_check.called == False
    assert test_mocker.post_check.call_count == 0
    assert test_mocker.close_client.called == False
    assert test_mocker.close_client.call_count == 0
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_run05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_run05 run試験05 異常系試験 (OK, mode:Mode.show, PreCheck異常)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.show
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がProcessStatus.pre_check_ngとなること
    ・open_clientが1回呼ばれること
    ・pre_checkが1回呼ばれること
    ・change_statusが0回呼ばれること
    ・post_checkが0回呼ばれること
    ・close_clientが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.show
    stub = False
    status = ProcessStatus.pre_check_ng

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.pre_check_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00330", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00331", [nf_name, f"process status: {status}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=True)
    test_mocker.pre_check = mocker.Mock(return_value=False)
    test_mocker.change_status = mocker.Mock(return_value=False)
    test_mocker.post_check = mocker.Mock(return_value=False)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker

    mocker.patch("time.sleep", test_mocker.sleep)
    mocker.patch.object(process, "open_client", test_mocker.open_client)
    mocker.patch.object(process, "pre_check", test_mocker.pre_check)
    mocker.patch.object(process, "change_status", test_mocker.change_status)
    mocker.patch.object(process, "post_check", test_mocker.post_check)
    mocker.patch.object(process, "close_client", test_mocker.close_client)

    response_value = process.run()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.open_client.called == True
    assert test_mocker.open_client.call_count == 1
    assert test_mocker.pre_check.called == True
    assert test_mocker.pre_check.call_count == 1
    assert test_mocker.change_status.called == False
    assert test_mocker.change_status.call_count == 0
    assert test_mocker.post_check.called == False
    assert test_mocker.post_check.call_count == 0
    assert test_mocker.close_client.called == True
    assert test_mocker.close_client.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_run06(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_run06 run試験06 異常系試験 (OK, mode:Mode.up, ChangeStatus異常)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がProcessStatus.change_ngとなること
    ・open_clientが1回呼ばれること
    ・pre_checkが1回呼ばれること
    ・change_statusが1回呼ばれること
    ・post_checkが0回呼ばれること
    ・close_clientが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    stub = False
    status = ProcessStatus.change_ng

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.change_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00330", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00331", [nf_name, f"process status: {status}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=True)
    test_mocker.pre_check = mocker.Mock(return_value=True)
    test_mocker.change_status = mocker.Mock(return_value=False)
    test_mocker.post_check = mocker.Mock(return_value=False)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    process.is_need_to_change = True
    mocker.patch("time.sleep", test_mocker.sleep)
    mocker.patch.object(process, "open_client", test_mocker.open_client)
    mocker.patch.object(process, "pre_check", test_mocker.pre_check)
    mocker.patch.object(process, "change_status", test_mocker.change_status)
    mocker.patch.object(process, "post_check", test_mocker.post_check)
    mocker.patch.object(process, "close_client", test_mocker.close_client)

    response_value = process.run()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.open_client.called == True
    assert test_mocker.open_client.call_count == 1
    assert test_mocker.pre_check.called == True
    assert test_mocker.pre_check.call_count == 1
    assert test_mocker.change_status.called == True
    assert test_mocker.change_status.call_count == 1
    assert test_mocker.post_check.called == False
    assert test_mocker.post_check.call_count == 0
    assert test_mocker.close_client.called == True
    assert test_mocker.close_client.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_run07(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_run07 run試験07 異常系試験 (OK, mode:Mode.up, PostCheck異常)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がProcessStatus.post_check_okとなること
    ・open_clientが1回呼ばれること
    ・pre_checkが1回呼ばれること
    ・change_statusが1回呼ばれること
    ・post_checkが1回呼ばれること
    ・close_clientが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    stub = False
    status = ProcessStatus.post_check_ng

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.post_check_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00330", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00331", [nf_name, f"process status: {status}"])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=True)
    test_mocker.pre_check = mocker.Mock(return_value=True)
    test_mocker.change_status = mocker.Mock(return_value=True)
    test_mocker.post_check = mocker.Mock(return_value=False)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    process.is_need_to_change = True
    mocker.patch("time.sleep", test_mocker.sleep)
    mocker.patch.object(process, "open_client", test_mocker.open_client)
    mocker.patch.object(process, "pre_check", test_mocker.pre_check)
    mocker.patch.object(process, "change_status", test_mocker.change_status)
    mocker.patch.object(process, "post_check", test_mocker.post_check)
    mocker.patch.object(process, "close_client", test_mocker.close_client)

    response_value = process.run()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.open_client.called == True
    assert test_mocker.open_client.call_count == 1
    assert test_mocker.pre_check.called == True
    assert test_mocker.pre_check.call_count == 1
    assert test_mocker.change_status.called == True
    assert test_mocker.change_status.call_count == 1
    assert test_mocker.post_check.called == True
    assert test_mocker.post_check.call_count == 1
    assert test_mocker.close_client.called == True
    assert test_mocker.close_client.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_run08(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_run08 run試験08 異常系試験 (OK, mode:Mode.up, Exception発生)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・mode = Mode.up
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がProcessStatus.exception_ngとなること
    ・open_clientが1回呼ばれること
    ・pre_checkが1回呼ばれること
    ・change_statusが0回呼ばれること
    ・post_checkが0回呼ばれること
    ・close_clientが0回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    mode = Mode.up
    stub = False
    status = ProcessStatus.exception_ng

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.exception_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00330", nf_name),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00331", [nf_name, f"process status: {status}"])
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:registration status変更プロセス異常:\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" ステータス: {ProcessStatus.exception_ng}\n",
        f" Trace: Exception Test Exception\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.eri_smf_registration_process.LOGGER", new=logger)
    mocker.patch("src.abc_eri_registration_process.NFShellClient", new=TestClient)
    mocker.patch("src.abc_eri_registration_process.StubClient", new=TestStubClient)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=True)
    test_mocker.pre_check = mocker.Mock(side_effect=Exception("Test Exception"))
    test_mocker.change_status = mocker.Mock(return_value=False)
    test_mocker.post_check = mocker.Mock(return_value=False)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    process = EriSmfRegistrationProcess(edns_host, nf_name, mode, stub)
    process._AbcEricssonRegistrationProcess__client = test_mocker
    process.is_need_to_change = None
    mocker.patch("time.sleep", test_mocker.sleep)
    mocker.patch.object(process, "open_client", test_mocker.open_client)
    mocker.patch.object(process, "pre_check", test_mocker.pre_check)
    mocker.patch.object(process, "change_status", test_mocker.change_status)
    mocker.patch.object(process, "post_check", test_mocker.post_check)
    mocker.patch.object(process, "close_client", test_mocker.close_client)

    response_value = process.run()

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
    assert test_mocker.open_client.called == True
    assert test_mocker.open_client.call_count == 1
    assert test_mocker.pre_check.called == True
    assert test_mocker.pre_check.call_count == 1
    assert test_mocker.change_status.called == False
    assert test_mocker.change_status.call_count == 0
    assert test_mocker.post_check.called == False
    assert test_mocker.post_check.call_count == 0
    assert test_mocker.close_client.called == True
    assert test_mocker.close_client.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd
