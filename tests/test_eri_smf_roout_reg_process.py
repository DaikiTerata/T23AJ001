import pathlib
from typing import Any, List
import pytest
from pytest_mock import MockerFixture
from datetime import datetime

from xgnlog.Log import Level
from src.abc_process import Status
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

    process = EriSmfRooutRegistrationProcess(edns_host, nf_name, mode, stub)
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

    expected_value = "nf-status undiscoverable"

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

    process = EriSmfRooutRegistrationProcess(edns_host, nf_name, mode, stub)
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

    process = EriSmfRooutRegistrationProcess(edns_host, nf_name, mode, stub)
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

    process = EriSmfRooutRegistrationProcess(edns_host, nf_name, mode, stub)
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

    expected_value = "epg pgw sbi smf-service nf-status undiscoverable"

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

    process = EriSmfRooutRegistrationProcess(edns_host, nf_name, mode, stub)
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

    process = EriSmfRooutRegistrationProcess(edns_host, nf_name, mode, stub)
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

    process = EriSmfRooutRegistrationProcess(edns_host, nf_name, mode, stub)
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

    process = EriSmfRooutRegistrationProcess(edns_host, nf_name, mode, stub)
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

    expected_value = "undiscoverable"

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

    process = EriSmfRooutRegistrationProcess(edns_host, nf_name, mode, stub)
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

    process = EriSmfRooutRegistrationProcess(edns_host, nf_name, mode, stub)
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
