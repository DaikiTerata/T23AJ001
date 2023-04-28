import pathlib
from typing import Any, List
from datetime import datetime

import pytest
from pytest_mock import MockerFixture
from xgnlog.Log import Level

from src.abc_process import Mode, ProcessStatus, TargetStatus
from src.eri_connection import SocketTimeoutException
from src.eri_smfvo_xcap_process import EriSmfvoXCAPProcess

JOB_ID = "T23AJ003"


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


class ClientForTest():
    def __init__(self, name: str):
        pass


class StubClientForTest():
    def __init__(self, mode: Mode, name: str):
        pass


def test_edns_ipaddr01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_edns_ipaddr01 edns_ipaddr試験01 edns_ipaddrプロパティ取得

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False

    試験結果
    ・インスタンス生成が正常に終了すること
    ・edns_ipaddrが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False

    expected_value = edns_ipaddr

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    response_value = process.edns_ipaddr

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, EriSmfvoXCAPProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_add_ipaddr01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_add_ipaddr01 add_ipaddr試験01 add_ipaddrプロパティ取得

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・add_ipaddr = "2001:268:200d:500f::6"

    試験結果
    ・インスタンス生成が正常に終了すること
    ・add_ipaddrが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    add_ipaddr = "2001:268:200d:500f::6"

    expected_value = add_ipaddr

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process.add_ipaddr = add_ipaddr
    response_value = process.add_ipaddr

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, EriSmfvoXCAPProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_priority01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_priority01 priority試験01 priorityプロパティ取得

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・priority = "100"

    試験結果
    ・インスタンス生成が正常に終了すること
    ・priorityが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    priority = "100"

    expected_value = priority

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process.priority = priority
    response_value = process.priority

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, EriSmfvoXCAPProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_ipaddr_list01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_ipaddr_list01 ipaddr_list試験01 ipaddr_listプロパティ取得

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False

    試験結果
    ・インスタンス生成が正常に終了すること
    ・ipaddr_listが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False

    expected_value = ipaddr_list

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    response_value = process.ipaddr_list

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    assert process is not None
    assert isinstance(process, EriSmfvoXCAPProcess)
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
    assert response_value == expected_value


def test_get_command01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_command01 get_command試験01 正常系試験 (Mode:down)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・downコマンドが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False

    expected_value = "no epg pgw apn xcap ipv6-name-server 2001:268:200d:1010::6"

    expected_sout = []

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
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
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.up
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・add_ipaddr = "2001:268:200d:500f::6"
    ・priority = "100"

    試験結果
    ・Exceptionが発生しないこと
    ・upコマンドが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.up
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    add_ipaddr = "2001:268:200d:500f::6"
    priority = "100"

    expected_value = "epg pgw apn xcap ipv6-name-server 2001:268:200d:500f::6 priority 100"

    expected_sout = []

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process.add_ipaddr = add_ipaddr
    process.priority = priority

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
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.show
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・showコマンドが取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.show
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False

    expected_value = "show running-config epg pgw apn xcap ipv6-name-server"

    expected_sout = []

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
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
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = None
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・コマンドが取得できないこと
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = None
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False

    expected_value = None

    expected_sout = []

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
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


def test_get_status_word01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_status_word01 get_status_word試験01 正常系試験 (Status:down)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・status = TargetStatus.down

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がout of useとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    status = TargetStatus.down

    expected_value = "out of use"

    expected_sout = []

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    response_value = process.get_status_word(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_get_status_word02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_status_word02 get_status_word試験02 正常系試験 (TargetStatus:up)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・status = TargetStatus.up

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がin useとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    status = TargetStatus.up

    expected_value = "in use"

    expected_sout = []

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    response_value = process.get_status_word(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_get_status_word03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_status_word03 get_status_word試験03 異常系試験 (Status:unknown)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・status = Status.unknown

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がunknownとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    status = TargetStatus.unknown

    expected_value = "unknown"

    expected_sout = []

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    response_value = process.get_status_word(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_get_commit_comment01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_commit_comment01 get_commit_comment試験01 正常系試験 (Mode:down)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果が19941203123456_xcap_eDNS_Changeとなること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False

    expected_value = "19941203123456_xcap_eDNS_Change"

    logtime = datetime(1994, 12, 3, 12, 34, 56)

    expected_sout = []

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    response_value = process.get_commit_comment()

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
    """test_get_status01 get_status試験01 正常系試験 (TargetStatus.up)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・status = TargetStatus.up

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTargetStatus.upとなること
    ・get_commandが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    status = TargetStatus.up

    send_command = [
        "show running-config epg pgw apn xcap ipv6-name-server"
    ]

    command_response_value = [
        "epg pgw apn xcap\n ipv6-name-server 2001:268:200d:1010::6\n  priority 100\n !\n ipv6-name-server 2001:268:200d:5010::6\n  priority 200\n !\n!".encode("utf-8")  # show run
    ]

    expected_value = TargetStatus.up

    logtime = datetime(1994, 12, 3, 12, 34, 56)

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00321, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:{send_command[0]}\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[0].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:I00322, add_info:{[nf_name, status]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.command = mocker.Mock(side_effect=[*command_response_value])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
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
    assert test_mocker.get_command.called == True
    assert test_mocker.get_command.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_status02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_status02 get_status試験02 正常系試験 (TargetStatus.down)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・status = TargetStatus.down

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTargetStatus.downとなること
    ・get_commandが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    status = TargetStatus.down

    send_command = [
        "show running-config epg pgw apn xcap ipv6-name-server"
    ]

    command_response_value = [
        "epg pgw apn xcap\n ipv6-name-server 2001:268:200d:500f::6\n  priority 100\n !\n ipv6-name-server 2001:268:200d:5010::6\n  priority 200\n !\n!".encode("utf-8")  # show run
    ]

    expected_value = TargetStatus.down

    logtime = datetime(1994, 12, 3, 12, 34, 56)

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00321, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:{send_command[0]}\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[0].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:I00322, add_info:{[nf_name, status]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.command = mocker.Mock(side_effect=[*command_response_value])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
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
    assert test_mocker.get_command.called == True
    assert test_mocker.get_command.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_status03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_status03 get_status試験03 異常系試験 (SocketTimeoutException発生)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・status = None
    ・SocketTimeoutException発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がNoneとなること
    ・get_commandが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    status = None

    send_command = [
        "show running-config epg pgw sbi smf-service nf-status"
    ]

    command_response_value = []

    expected_value = None

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        "ssh connection timeout was happened. [ UNKNOWN ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00321, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:{send_command[0]}\n",
        f"job_id:{JOB_ID}, message_id:E00304, add_info:{nf_name}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:xCAP ipaddr状態取得失敗:\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: {send_command[0]}\n",
        f" Trace: SocketTimeoutException Test SocketTimeoutException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.command = mocker.Mock(side_effect=[SocketTimeoutException("Test SocketTimeoutException")])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
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
    assert test_mocker.get_command.called == True
    assert test_mocker.get_command.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_get_status04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_status04 get_status試験04 異常系試験 (Exception発生)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・status = None
    ・Exception発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がNoneとなること
    ・get_commandが1回呼ばれること
    ・client.commandが1回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    status = None

    send_command = [
        "show running-config epg pgw sbi smf-service nf-status"
    ]

    command_response_value = []

    expected_value = None

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        "unexpected error occurred. [ UNKNOWN ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00321, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:{send_command[0]}\n",
        f"job_id:{JOB_ID}, message_id:E00304, add_info:{nf_name}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:xCAP ipaddr状態取得失敗:\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: {send_command[0]}\n",
        f" Trace: Exception Test Exception\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.command = mocker.Mock(side_effect=[Exception("Test Exception")])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
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
    assert test_mocker.get_command.called == True
    assert test_mocker.get_command.call_count == 1
    assert test_mocker.command.called == True
    assert test_mocker.command.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_change_status01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_change_status01 change_status試験01 正常系試験 (ProcessStatus.commit_ok)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・get_status_word = "in use"
    ・add_ipaddr = "2001:268:200d:500f::6"
    ・priority = "100"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がProcessStatus.commit_okとなること
    ・parse_resultが1回呼ばれること
    ・get_status_wordが呼ばれるないこと
    ・to_downが1回呼ばれること
    ・to_upが1回呼ばれること
    ・commitが1回呼ばれること
    ・do_abortが呼ばれるないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    get_status_word = "in use"
    add_ipaddr = "2001:268:200d:500f::6"
    priority = "100"

    command_response_value = []

    expected_value = ProcessStatus.commit_ok

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00323, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00324, add_info:{nf_name}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.parse_result = mocker.Mock(return_value=None)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)
    test_mocker.to_down = mocker.Mock(return_value=True)
    test_mocker.to_up = mocker.Mock(return_value=True)
    test_mocker.commit = mocker.Mock(return_value=True)
    test_mocker.do_abort = mocker.Mock(return_value=True)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.change_status", test_mocker.change_status)
    mocker.patch("src.abc_eri_process.AbcEricssonProcess.commit", test_mocker.commit)
    mocker.patch("src.abc_eri_process.AbcEricssonProcess.do_abort", test_mocker.do_abort)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.add_ipaddr = add_ipaddr
    process.priority = priority

    mocker.patch.object(process, "parse_result", test_mocker.parse_result)
    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)
    mocker.patch.object(process, "to_down", test_mocker.to_down)
    mocker.patch.object(process, "to_up", test_mocker.to_up)

    response_value = process.change_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.parse_result.called == True
    assert test_mocker.parse_result.call_count == 1
    assert test_mocker.get_status_word.called == False
    assert test_mocker.get_status_word.call_count == 0
    assert test_mocker.to_down.called == True
    assert test_mocker.to_down.call_count == 1
    assert test_mocker.to_up.called == True
    assert test_mocker.to_up.call_count == 1
    assert test_mocker.commit.called == True
    assert test_mocker.commit.call_count == 1
    assert test_mocker.do_abort.called == False
    assert test_mocker.do_abort.call_count == 0
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_change_status02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_change_status02 change_status試験02 準正常系試験 (ProcessStatus.change_ng, 追加IPアドレスなし)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・get_status_word = "in use"
    ・before_status = TargetStatus.up
    ・add_ipaddr = None
    ・priority = "100"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がProcessStatus.change_ngとなること
    ・parse_resultが1回呼ばれること
    ・get_status_wordが1回呼ばれること
    ・to_downが呼ばれるないこと
    ・to_upが呼ばれるないこと
    ・commitが呼ばれるないこと
    ・do_abortが呼ばれるないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    get_status_word = "in use"
    before_status = TargetStatus.up
    add_ipaddr = None
    priority = "100"

    command_response_value = []

    expected_value = ProcessStatus.change_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        "xcap ipaddr change was failed due to no reserved ipaddr. current status is"
        f" {get_status_word}. [ {before_status} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00323, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:E00321, add_info:{[nf_name, mode]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.parse_result = mocker.Mock(return_value=None)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)
    test_mocker.to_down = mocker.Mock(return_value=True)
    test_mocker.to_up = mocker.Mock(return_value=True)
    test_mocker.commit = mocker.Mock(return_value=True)
    test_mocker.do_abort = mocker.Mock(return_value=True)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.change_status", test_mocker.change_status)
    mocker.patch("src.abc_eri_process.AbcEricssonProcess.commit", test_mocker.commit)
    mocker.patch("src.abc_eri_process.AbcEricssonProcess.do_abort", test_mocker.do_abort)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.add_ipaddr = add_ipaddr
    process.priority = priority
    process.before_status = before_status

    mocker.patch.object(process, "parse_result", test_mocker.parse_result)
    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)
    mocker.patch.object(process, "to_down", test_mocker.to_down)
    mocker.patch.object(process, "to_up", test_mocker.to_up)

    response_value = process.change_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.parse_result.called == True
    assert test_mocker.parse_result.call_count == 1
    assert test_mocker.get_status_word.called == True
    assert test_mocker.get_status_word.call_count == 1
    assert test_mocker.to_down.called == False
    assert test_mocker.to_down.call_count == 0
    assert test_mocker.to_up.called == False
    assert test_mocker.to_up.call_count == 0
    assert test_mocker.commit.called == False
    assert test_mocker.commit.call_count == 0
    assert test_mocker.do_abort.called == False
    assert test_mocker.do_abort.call_count == 0
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_change_status03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_change_status03 change_status試験03 準正常系試験 (ProcessStatus.change_ng, to_down失敗)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・get_status_word = "in use"
    ・before_status = TargetStatus.up
    ・add_ipaddr = "2001:268:200d:500f::6"
    ・priority = "100"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がProcessStatus.change_ngとなること
    ・parse_resultが1回呼ばれること
    ・get_status_wordが1回呼ばれること
    ・to_downが1回呼ばれること
    ・to_upが呼ばれるないこと
    ・commitが呼ばれるないこと
    ・do_abortが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    get_status_word = "in use"
    before_status = TargetStatus.up
    add_ipaddr = "2001:268:200d:500f::6"
    priority = "100"

    command_response_value = []

    expected_value = ProcessStatus.change_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        f"xcap ipaddr change was failed. abort has done. current status is"
        f" {get_status_word}. [ {before_status} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00323, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:E00321, add_info:{[nf_name, mode]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.parse_result = mocker.Mock(return_value=None)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)
    test_mocker.to_down = mocker.Mock(return_value=False)
    test_mocker.to_up = mocker.Mock(return_value=True)
    test_mocker.commit = mocker.Mock(return_value=True)
    test_mocker.do_abort = mocker.Mock(return_value=True)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.change_status", test_mocker.change_status)
    mocker.patch("src.abc_eri_process.AbcEricssonProcess.commit", test_mocker.commit)
    mocker.patch("src.abc_eri_process.AbcEricssonProcess.do_abort", test_mocker.do_abort)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.add_ipaddr = add_ipaddr
    process.priority = priority
    process.before_status = before_status

    mocker.patch.object(process, "parse_result", test_mocker.parse_result)
    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)
    mocker.patch.object(process, "to_down", test_mocker.to_down)
    mocker.patch.object(process, "to_up", test_mocker.to_up)

    response_value = process.change_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.parse_result.called == True
    assert test_mocker.parse_result.call_count == 1
    assert test_mocker.get_status_word.called == True
    assert test_mocker.get_status_word.call_count == 1
    assert test_mocker.to_down.called == True
    assert test_mocker.to_down.call_count == 1
    assert test_mocker.to_up.called == False
    assert test_mocker.to_up.call_count == 0
    assert test_mocker.commit.called == False
    assert test_mocker.commit.call_count == 0
    assert test_mocker.do_abort.called == True
    assert test_mocker.do_abort.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_change_status04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_change_status04 change_status試験04 準正常系試験 (ProcessStatus.change_ng, to_up失敗)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・get_status_word = "in use"
    ・before_status = TargetStatus.up
    ・add_ipaddr = "2001:268:200d:500f::6"
    ・priority = "100"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・parse_resultが1回呼ばれること
    ・get_status_wordが1回呼ばれること
    ・to_downが1回呼ばれること
    ・to_upが1回呼ばれること
    ・commitが呼ばれるないこと
    ・do_abortが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    get_status_word = "in use"
    before_status = TargetStatus.up
    add_ipaddr = "2001:268:200d:500f::6"
    priority = "100"

    command_response_value = []

    expected_value = ProcessStatus.change_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        f"xcap ipaddr change was failed. abort has done. current status is"
        f" {get_status_word}. [ {before_status} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00323, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:E00321, add_info:{[nf_name, mode]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.parse_result = mocker.Mock(return_value=None)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)
    test_mocker.to_down = mocker.Mock(return_value=True)
    test_mocker.to_up = mocker.Mock(return_value=False)
    test_mocker.commit = mocker.Mock(return_value=True)
    test_mocker.do_abort = mocker.Mock(return_value=True)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.change_status", test_mocker.change_status)
    mocker.patch("src.abc_eri_process.AbcEricssonProcess.commit", test_mocker.commit)
    mocker.patch("src.abc_eri_process.AbcEricssonProcess.do_abort", test_mocker.do_abort)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.add_ipaddr = add_ipaddr
    process.priority = priority
    process.before_status = before_status

    mocker.patch.object(process, "parse_result", test_mocker.parse_result)
    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)
    mocker.patch.object(process, "to_down", test_mocker.to_down)
    mocker.patch.object(process, "to_up", test_mocker.to_up)

    response_value = process.change_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.parse_result.called == True
    assert test_mocker.parse_result.call_count == 1
    assert test_mocker.get_status_word.called == True
    assert test_mocker.get_status_word.call_count == 1
    assert test_mocker.to_down.called == True
    assert test_mocker.to_down.call_count == 1
    assert test_mocker.to_up.called == True
    assert test_mocker.to_up.call_count == 1
    assert test_mocker.commit.called == False
    assert test_mocker.commit.call_count == 0
    assert test_mocker.do_abort.called == True
    assert test_mocker.do_abort.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_change_status05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_change_status05 change_status試験05 準正常系試験 (ProcessStatus.commit_ng, commit失敗)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・get_status_word = "in use"
    ・before_status = TargetStatus.up
    ・add_ipaddr = "2001:268:200d:500f::6"
    ・priority = "100"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・parse_resultが1回呼ばれること
    ・get_status_wordが呼ばれるないこと
    ・to_downが1回呼ばれること
    ・to_upが1回呼ばれること
    ・commitが1回呼ばれること
    ・do_abortが1回呼ばれること

    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    get_status_word = "in use"
    before_status = TargetStatus.up
    add_ipaddr = "2001:268:200d:500f::6"
    priority = "100"

    command_response_value = []

    expected_value = ProcessStatus.commit_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        "commit was failed. abort has done.\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00323, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:E00322, add_info:{[nf_name, mode]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.parse_result = mocker.Mock(return_value=None)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)
    test_mocker.to_down = mocker.Mock(return_value=True)
    test_mocker.to_up = mocker.Mock(return_value=True)
    test_mocker.commit = mocker.Mock(return_value=False)
    test_mocker.do_abort = mocker.Mock(return_value=True)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.change_status", test_mocker.change_status)
    mocker.patch("src.abc_eri_process.AbcEricssonProcess.commit", test_mocker.commit)
    mocker.patch("src.abc_eri_process.AbcEricssonProcess.do_abort", test_mocker.do_abort)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.add_ipaddr = add_ipaddr
    process.priority = priority
    process.before_status = before_status

    mocker.patch.object(process, "parse_result", test_mocker.parse_result)
    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)
    mocker.patch.object(process, "to_down", test_mocker.to_down)
    mocker.patch.object(process, "to_up", test_mocker.to_up)

    response_value = process.change_status()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.parse_result.called == True
    assert test_mocker.parse_result.call_count == 1
    assert test_mocker.get_status_word.called == False
    assert test_mocker.get_status_word.call_count == 0
    assert test_mocker.to_down.called == True
    assert test_mocker.to_down.call_count == 1
    assert test_mocker.to_up.called == True
    assert test_mocker.to_up.call_count == 1
    assert test_mocker.commit.called == True
    assert test_mocker.commit.call_count == 1
    assert test_mocker.do_abort.called == True
    assert test_mocker.do_abort.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_to_down01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_to_down01 to_down試験01 正常系試験 (OK)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
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
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False

    send_command = [
        "no epg pgw apn xcap ipv6-name-server 2001:268:200d:1010::6"
    ]

    command_response_value = [
        "\n".encode("utf-8")  # deregistered
    ]

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00325, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:config\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:{send_command[0]}\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[0].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:I00326, add_info:{[nf_name, mode, True]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=command_response_value)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.to_down()

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


def test_to_down02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_to_down02 to_down試験02 異常系試験 (NG, SocketTimeoutException発生)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・SocketTimeoutException発生

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
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False

    send_command = [
        "no epg pgw apn xcap ipv6-name-server 2001:268:200d:1010::6"
    ]

    command_response_value = [
        "\n".encode("utf-8")  # deregistered
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        "ssh connection timeout was happened. [ UNKNOWN ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00325, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:config\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:{send_command[0]}\n",
        f"job_id:{JOB_ID}, message_id:E00303, add_info:{[nf_name, mode]}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:xCAP ipaddr削除変更異常:\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: {send_command[0]}\n",
        f" Trace: SocketTimeoutException Test SocketTimeoutException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[SocketTimeoutException("Test SocketTimeoutException")])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.to_down()

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


def test_to_down03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_to_down03 to_down試験03 異常系試験 (NG, その他Exception発生)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・Exception発生

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
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False

    send_command = [
        "no epg pgw apn xcap ipv6-name-server 2001:268:200d:1010::6"
    ]

    command_response_value = [
        "\n".encode("utf-8")  # deregistered
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        "unexpected error occurred. [ UNKNOWN ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00325, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:config\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:{send_command[0]}\n",
        f"job_id:{JOB_ID}, message_id:E00303, add_info:{[nf_name, mode]}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:xCAP ipaddr削除変更異常:\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: {send_command[0]}\n",
        f" Trace: Exception Test Exception\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[Exception("Test Exception")])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.to_down()

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


def test_to_up01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_to_up01 to_up試験01 正常系試験 (OK)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
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
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False

    send_command = [
        "epg pgw apn xcap ipv6-name-server 2001:268:200d:500f::6 priority 100"
    ]

    command_response_value = [
        "\n".encode("utf-8")  # registered
    ]

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00327, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:config\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:{send_command[0]}\n",
        *f"job_id:{JOB_ID}, message_id:I00310, add_info:{command_response_value[0].decode('utf-8')}\n".splitlines(True),
        f"job_id:{JOB_ID}, message_id:I00328, add_info:{[nf_name, mode, True]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=command_response_value)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.to_up()

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


def test_to_up02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_to_up02 to_up試験02 異常系試験 (NG, SocketTimeoutException発生)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・SocketTimeoutException発生

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
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False

    send_command = [
        "epg pgw apn xcap ipv6-name-server 2001:268:200d:500f::6 priority 100"
    ]

    command_response_value = [
        "\n".encode("utf-8")  # registered
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        "ssh connection timeout was happened. [ UNKNOWN ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00327, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:config\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:{send_command[0]}\n",
        f"job_id:{JOB_ID}, message_id:E00303, add_info:{[nf_name, mode]}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:xCAP ipaddr追加変更異常:\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: {send_command[0]}\n",
        f" Trace: SocketTimeoutException Test SocketTimeoutException\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[SocketTimeoutException("Test SocketTimeoutException")])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.to_up()

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


def test_to_up03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_to_up03 to_up試験03 異常系試験 (その他Exception発生)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・Exception発生

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
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False

    send_command = [
        "epg pgw apn xcap ipv6-name-server 2001:268:200d:500f::6 priority 100"
    ]

    command_response_value = [
        "\n".encode("utf-8")  # registered
    ]

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        "unexpected error occurred. [ UNKNOWN ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00327, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:config\n",
        f"job_id:{JOB_ID}, message_id:I00310, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00309, add_info:{send_command[0]}\n",
        f"job_id:{JOB_ID}, message_id:E00303, add_info:{[nf_name, mode]}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:xCAP ipaddr追加変更異常:\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" コマンド: {send_command[0]}\n",
        f" Trace: Exception Test Exception\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.get_command = mocker.Mock(return_value=send_command[0])
    test_mocker.enter_config_mode = mocker.Mock(return_value=None)
    test_mocker.command = mocker.Mock(side_effect=[Exception("Test Exception")])

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    mocker.patch.object(process, "get_command", test_mocker.get_command)

    response_value = process.to_up()

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


def test_pre_check01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_pre_check01 pre_check試験01 正常系試験 (pre_check: True)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・super_pre_check = True

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・AbcProcess.pre_checkが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    super_pre_check = True

    command_response_value = []

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00329, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00330, add_info:{[nf_name, 'pre_check: True']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.pre_check = mocker.Mock(return_value=super_pre_check)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.pre_check", test_mocker.pre_check)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    response_value = process.pre_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.pre_check.called == True
    assert test_mocker.pre_check.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_pre_check02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_pre_check02 pre_check試験02 正常系試験 (pre_check: False)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・super_pre_check = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・AbcProcess.pre_checkが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    super_pre_check = False

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00329, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00330, add_info:{[nf_name, 'pre_check: False']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.pre_check = mocker.Mock(return_value=super_pre_check)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.pre_check", test_mocker.pre_check)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    response_value = process.pre_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.pre_check.called == True
    assert test_mocker.pre_check.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_post_check01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_post_check01 post_check試験01 正常系試験 (post_check: True)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・super_post_check = True

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・AbcProcess.post_checkが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    super_post_check = True

    command_response_value = []

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00331, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00332, add_info:{[nf_name, 'post_check: True']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.post_check = mocker.Mock(return_value=super_post_check)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.post_check", test_mocker.post_check)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    response_value = process.post_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.post_check.called == True
    assert test_mocker.post_check.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_post_check02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_post_check02 post_check試験02 準正常系試験 (post_check: False)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・stub = False
    ・super_post_check = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・AbcProcess.post_checkが1回呼ばれること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    super_post_check = False

    command_response_value = []

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00331, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00332, add_info:{[nf_name, 'post_check: False']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.post_check = mocker.Mock(return_value=super_post_check)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.post_check", test_mocker.post_check)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    response_value = process.post_check()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.post_check.called == True
    assert test_mocker.post_check.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_necessity_check01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_necessity_check01 necessity_check試験01 正常系試験 (mode: Mode.show, status: TargetStatus.up, 変更不要)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.show
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・status = TargetStatus.up
    ・get_status_word = "in use"
    ・super_necessity_check = ProcessStatus.show_or_unknown

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がshow_or_unknownとなること
    ・AbcProcess.necessity_checkが1回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.show
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    status = TargetStatus.up
    get_status_word = "in use"
    super_necessity_check = ProcessStatus.show_or_unknown

    command_response_value = []

    expected_value = ProcessStatus.show_or_unknown

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[INFO]:{mode}:{logtime}:{edns_name}({nf_name}):"
        f"current xCAP ipaddr is {get_status_word}. [ {status} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00333, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00341, add_info:{[nf_name, mode, status]}\n",
        f"job_id:{JOB_ID}, message_id:I00334, add_info:{[nf_name, 'necessity: show_or_unknown']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.necessity_check = mocker.Mock(return_value=super_necessity_check)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.necessity_check", test_mocker.necessity_check)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.necessity_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.necessity_check.called == True
    assert test_mocker.necessity_check.call_count == 1
    assert test_mocker.get_status_word.called == True
    assert test_mocker.get_status_word.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_necessity_check02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_necessity_check02 necessity_check試験02 正常系試験 (mode: Mode.down, status: TargetStatus.down, 変更不要)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・status = TargetStatus.down
    ・get_status_word = "out of use"
    ・super_necessity_check = ProcessStatus.already_changed

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がalready_changedとなること
    ・AbcProcess.necessity_checkが1回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    status = TargetStatus.down
    get_status_word = "out of use"
    super_necessity_check = ProcessStatus.already_changed

    command_response_value = []

    expected_value = ProcessStatus.already_changed

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[SUCCESS]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        f"current xCAP ipaddr is already {get_status_word}. [ {status} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00333, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00341, add_info:{[nf_name, mode, status]}\n",
        f"job_id:{JOB_ID}, message_id:I00334, add_info:{[nf_name, 'necessity: already_changed']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.necessity_check = mocker.Mock(return_value=super_necessity_check)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.necessity_check", test_mocker.necessity_check)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.necessity_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.necessity_check.called == True
    assert test_mocker.necessity_check.call_count == 1
    assert test_mocker.get_status_word.called == True
    assert test_mocker.get_status_word.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_necessity_check03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_necessity_check03 necessity_check試験03 正常系試験 (mode: Mode.down, status: TargetStatus.up, 要変更)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・status = TargetStatus.up
    ・get_status_word = "in use"
    ・super_necessity_check = ProcessStatus.need_to_change

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がneed_to_changeとなること
    ・AbcProcess.necessity_checkが1回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    status = TargetStatus.up
    get_status_word = "registered"
    super_necessity_check = ProcessStatus.need_to_change

    command_response_value = []

    expected_value = ProcessStatus.need_to_change

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[INFO]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        f"current xCAP ipaddr is {get_status_word}. [ {status} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00333, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00342, add_info:{[nf_name, mode, status]}\n",
        f"job_id:{JOB_ID}, message_id:I00334, add_info:{[nf_name, 'necessity: need_to_change']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.necessity_check = mocker.Mock(return_value=super_necessity_check)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.necessity_check", test_mocker.necessity_check)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.necessity_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.necessity_check.called == True
    assert test_mocker.necessity_check.call_count == 1
    assert test_mocker.get_status_word.called == True
    assert test_mocker.get_status_word.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_necessity_check04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_necessity_check04 necessity_check試験04 異常系試験 (mode: Mode.down, status: None)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・status = None
    ・get_status_word = "in use"
    ・super_necessity_check = ProcessStatus.exception_ng

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がNoneとなること
    ・AbcProcess.necessity_checkが1回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    status = None
    get_status_word = "unknown"
    super_necessity_check = ProcessStatus.exception_ng

    command_response_value = []

    expected_value = ProcessStatus.exception_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        "currentry xCAP ipaddr couldn't get or mismatch. [ UNKNOWN ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00333, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:E00323, add_info:{[nf_name, mode, status]}\n",
        f"job_id:{JOB_ID}, message_id:I00334, add_info:{[nf_name, 'necessity: exception_ng']}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:xCAP ipaddr事前状態取得失敗:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" MODE: {mode}\n",
        f" STATUS: {status}\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.necessity_check = mocker.Mock(return_value=super_necessity_check)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.necessity_check", test_mocker.necessity_check)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger

    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.necessity_check(status)

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
    assert test_mocker.necessity_check.called == True
    assert test_mocker.necessity_check.call_count == 1
    assert test_mocker.get_status_word.called == False
    assert test_mocker.get_status_word.call_count == 0
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_changed_check01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_changed_check01 changed_check試験01 正常系試験 (mode: Mode.down, status: down, add_status: up, 変更OK)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・status = TargetStatus.down
    ・added_status = TargetStatus.up
    ・get_status_word = "out of use"
    ・status_result = "epg pgw apn xcap\n ipv6-name-server 2001:268:200d:5010::6\n  priority 200\n !\n ipv6-name-server 2001:268:200d:500f::6\n  priority 100\n !\n!"
    ・add_ipaddr = "2001:268:200d:500f::6"
    ・super_changed_check = ProcessStatus.change_ok

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がchange_okとなること
    ・AbcProcess.changed_checkが1回呼ばれること
    ・get_status_wordが1回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    status = TargetStatus.down
    added_status = TargetStatus.up
    get_status_word = "out of use"
    status_result = "epg pgw apn xcap\n ipv6-name-server 2001:268:200d:5010::6\n  priority 200\n !\n ipv6-name-server 2001:268:200d:500f::6\n  priority 100\n !\n!"
    add_ipaddr = "2001:268:200d:500f::6"
    super_changed_check = ProcessStatus.change_ok

    command_response_value = []

    expected_value = ProcessStatus.change_ok

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[SUCCESS]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        f"current xCAP ipaddr is {get_status_word}. [ {status} ]"
        f" reserved ipaddr added. [ {added_status} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00335, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00343, add_info:{[nf_name, mode, status, added_status]}\n",
        f"job_id:{JOB_ID}, message_id:I00336, add_info:{[nf_name, 'changed: change_ok']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.changed_check = mocker.Mock(return_value=super_changed_check)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.changed_check", test_mocker.changed_check)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.status_result = status_result
    process.add_ipaddr = add_ipaddr

    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.changed_check(status)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.changed_check.called == True
    assert test_mocker.changed_check.call_count == 1
    assert test_mocker.get_status_word.called == True
    assert test_mocker.get_status_word.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_changed_check02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_changed_check02 changed_check試験02 正常系試験 (mode: Mode.down, status: down, add_status: up, 変更OK)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・status = TargetStatus.down
    ・added_status = TargetStatus.down
    ・get_status_word = "in use"
    ・status_result = "epg pgw apn xcap\n ipv6-name-server 2001:268:200d:5010::6\n  priority 200\n !\n!"
    ・add_ipaddr = "2001:268:200d:500f::6"
    ・super_changed_check = ProcessStatus.change_ok

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がchange_ngとなること
    ・AbcProcess.changed_checkが1回呼ばれること
    ・get_status_wordが1回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    status = TargetStatus.down
    added_status = TargetStatus.down
    get_status_word = "in use"
    status_result = "epg pgw apn xcap\n ipv6-name-server 2001:268:200d:5010::6\n  priority 200\n !\n!"
    add_ipaddr = "2001:268:200d:500f::6"
    super_changed_check = ProcessStatus.change_ok

    command_response_value = []

    expected_value = ProcessStatus.change_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        f"current xCAP ipaddr is {get_status_word}. [ {status} ]"
        f" but reserved ipaddr couldn't add... [ {added_status} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00335, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:E00324, add_info:{[nf_name, mode, status, added_status]}\n",
        f"job_id:{JOB_ID}, message_id:I00336, add_info:{[nf_name, 'changed: change_ng']}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:xCAP ipaddr事後確認変更失敗:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" MODE: {mode}\n",
        f" STATUS: {status, added_status}\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.changed_check = mocker.Mock(return_value=super_changed_check)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.changed_check", test_mocker.changed_check)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.status_result = status_result
    process.add_ipaddr = add_ipaddr

    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.changed_check(status)

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
    assert test_mocker.changed_check.called == True
    assert test_mocker.changed_check.call_count == 1
    assert test_mocker.get_status_word.called == True
    assert test_mocker.get_status_word.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_changed_check03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_changed_check03 changed_check試験03 準正常系試験 (mode: Mode.down, status: Status.down, 変更失敗)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・status = TargetStatus.up
    ・added_status = TargetStatus.down
    ・get_status_word = "in use"
    ・status_result = "epg pgw apn xcap\n ipv6-name-server 2001:268:200d:1010::6\n  priority 100\n !\n ipv6-name-server 2001:268:200d:5010::6\n  priority 200\n !\n!"
    ・add_ipaddr = "2001:268:200d:500f::6"
    ・super_changed_check = ProcessStatus.change_ng

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がchange_ngとなること
    ・AbcProcess.changed_checkが1回呼ばれること
    ・get_status_wordが1回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    status = TargetStatus.up
    added_status = TargetStatus.down
    get_status_word = "in use"
    status_result = "epg pgw apn xcap\n ipv6-name-server 2001:268:200d:1010::6\n  priority 100\n !\n ipv6-name-server 2001:268:200d:5010::6\n  priority 200\n !\n!"
    add_ipaddr = "2001:268:200d:500f::6"
    super_changed_check = ProcessStatus.change_ng

    command_response_value = []

    expected_value = ProcessStatus.change_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({nf_name}):"
        f"xCAP ipaddr couldn't change... still {get_status_word}. [ {status} ]"
        f" reserved ipaddr [ {added_status} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00335, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:E00324, add_info:{[nf_name, mode, status, added_status]}\n",
        f"job_id:{JOB_ID}, message_id:I00336, add_info:{[nf_name, 'changed: change_ng']}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:xCAP ipaddr事後確認変更失敗:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" MODE: {mode}\n",
        f" STATUS: {status, added_status}\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.changed_check = mocker.Mock(return_value=super_changed_check)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.changed_check", test_mocker.changed_check)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.status_result = status_result
    process.add_ipaddr = add_ipaddr

    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.changed_check(status)

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
    assert test_mocker.changed_check.called == True
    assert test_mocker.changed_check.call_count == 1
    assert test_mocker.get_status_word.called == True
    assert test_mocker.get_status_word.call_count == 1
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_changed_check04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_changed_check04 changed_check試験04 異常系試験 (mode: Mode.down, status: Status.unknown, 変更異常)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・status = None
    ・added_status = TargetStatus.down
    ・get_status_word = "unknown"
    ・status_result = "error"
    ・add_ipaddr = "2001:268:200d:500f::6"
    ・super_changed_check = ProcessStatus.exception_ng

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がexception_ngとなること
    ・AbcProcess.changed_checkが1回呼ばれること
    ・get_status_wordが呼ばれないこと
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    status = None
    added_status = TargetStatus.down
    get_status_word = "unknown"
    status_result = "error"
    add_ipaddr = "2001:268:200d:500f::6"
    super_changed_check = ProcessStatus.exception_ng

    command_response_value = []

    expected_value = ProcessStatus.exception_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime}:{edns_name}({nf_name}):"
        "currentry xCAP ipaddr couldn't get or mismatch. [ UNKNOWN ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00335, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:E00323, add_info:{[nf_name, mode, status, added_status]}\n",
        f"job_id:{JOB_ID}, message_id:I00336, add_info:{[nf_name, 'changed: exception_ng']}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:xCAP ipaddr事後確認取得失敗:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" MODE: {mode}\n",
        f" STATUS: {status, added_status}\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    test_mocker = mocker.MagicMock()
    test_mocker.changed_check = mocker.Mock(return_value=super_changed_check)
    test_mocker.get_status_word = mocker.Mock(return_value=get_status_word)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    mocker.patch("src.abc_process.AbcProcess.changed_check", test_mocker.changed_check)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.status_result = status_result
    process.add_ipaddr = add_ipaddr

    mocker.patch.object(process, "get_status_word", test_mocker.get_status_word)

    response_value = process.changed_check(status)

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
    assert test_mocker.changed_check.called == True
    assert test_mocker.changed_check.call_count == 1
    assert test_mocker.get_status_word.called == False
    assert test_mocker.get_status_word.call_count == 0
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_parse_result01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_parse_result01 parse_result試験01 正常系試験 (追加IPアドレスあり)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・status_result = "epg pgw apn xcap\r\n ipv6-name-server 2001:268:200d:1010::6\r\n  priority 100\r\n !\r\n ipv6-name-server 2001:268:200d:5010::6\r\n  priority 200\r\n !\r\n!"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    status_result = "epg pgw apn xcap\r\n ipv6-name-server 2001:268:200d:1010::6\r\n  priority 100\r\n !\r\n ipv6-name-server 2001:268:200d:5010::6\r\n  priority 200\r\n !\r\n!"
    parsed_list = [
        {
            "ipaddr": "2001:268:200d:1010::6",
            "priority": "100"
        },
        {
            "ipaddr": "2001:268:200d:5010::6",
            "priority": "200"
        }
    ]
    add_ipaddr = "2001:268:200d:500f::6"
    priority = "100"

    command_response_value = []

    expected_value = None

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00337, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00338, add_info:{[nf_name, parsed_list, add_ipaddr, priority]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcProcess__logger = logger

    response_value = process.parse_result(status_result)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert process.add_ipaddr == add_ipaddr
    assert process.priority == priority
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_parse_result02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_parse_result02 parse_result試験02 正常系試験 (追加IPアドレスあり)

    試験条件
    ・edns_name = "tys1tb3edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:500f::6"
    ・ipaddr_list = [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    ・status_result = "epg pgw apn xcap\r\n ipv6-name-server 2001:268:200d:5010::6\r\n  priority 200\r\n !\r\n ipv6-name-server 2001:268:200d:500f::6\r\n  priority 100\r\n !\r\n!"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb3edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:500f::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    status_result = "epg pgw apn xcap\r\n ipv6-name-server 2001:268:200d:5010::6\r\n  priority 200\r\n !\r\n ipv6-name-server 2001:268:200d:500f::6\r\n  priority 100\r\n !\r\n!"
    parsed_list = [
        {
            "ipaddr": "2001:268:200d:5010::6",
            "priority": "200"
        },
        {
            "ipaddr": "2001:268:200d:500f::6",
            "priority": "100"
        }
    ]
    add_ipaddr = "2001:268:200d:1010::6"
    priority = "100"

    command_response_value = []

    expected_value = None

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00337, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00338, add_info:{[nf_name, parsed_list, add_ipaddr, priority]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcProcess__logger = logger

    response_value = process.parse_result(status_result)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert process.add_ipaddr == add_ipaddr
    assert process.priority == priority
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_parse_result03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_parse_result03 parse_result試験03 準正常系試験 (追加IPアドレスなし)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6"
    ]
    ・status_result = "epg pgw apn xcap\r\n ipv6-name-server 2001:268:200d:1010::6\r\n  priority 100\r\n !\r\n ipv6-name-server 2001:268:200d:5010::6\r\n  priority 200\r\n !\r\n!"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6"
    ]
    status_result = "epg pgw apn xcap\r\n ipv6-name-server 2001:268:200d:1010::6\r\n  priority 100\r\n !\r\n ipv6-name-server 2001:268:200d:5010::6\r\n  priority 200\r\n !\r\n!"
    parsed_list = [
        {
            "ipaddr": "2001:268:200d:1010::6",
            "priority": "100"
        },
        {
            "ipaddr": "2001:268:200d:5010::6",
            "priority": "200"
        }
    ]
    add_ipaddr = None
    priority = "100"

    command_response_value = []

    expected_value = None

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00337, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00338, add_info:{[nf_name, parsed_list, add_ipaddr, priority]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcProcess__logger = logger

    response_value = process.parse_result(status_result)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert process.add_ipaddr == add_ipaddr
    assert process.priority == priority
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_parse_result04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_parse_result04 parse_result試験04 準正常系試験 (追加IPアドレスなし)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    ・status_result = "error"

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    status_result = "error"
    parsed_list = []
    add_ipaddr = None
    priority = None

    command_response_value = []

    expected_value = None

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00337, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00338, add_info:{[nf_name, parsed_list, add_ipaddr, priority]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, JOB_ID)
    process._AbcProcess__logger = logger

    response_value = process.parse_result(status_result)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert process.add_ipaddr == add_ipaddr
    assert process.priority == priority
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_run01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_run01 run試験01 正常系試験 (OK, mode:Mode.down)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    ・stub = False
    ・open_client = True
    ・pre_check = True
    ・necessity = ProcessStatus.need_to_change
    ・change_status = ProcessStatus.commit_ok
    ・post_check = True

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
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    open_client = True
    pre_check = True
    necessity = ProcessStatus.need_to_change
    change_status = ProcessStatus.commit_ok
    post_check = True

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.post_check_ok

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00339, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00340, add_info:{[nf_name, 'process status: post_check_ok']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=open_client)
    test_mocker.pre_check = mocker.Mock(return_value=pre_check)
    test_mocker.change_status = mocker.Mock(return_value=change_status)
    test_mocker.post_check = mocker.Mock(return_value=post_check)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.necessity = necessity
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
    """test_run02 run試験02 正常系試験 (OK, mode:Mode.show)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.show
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    ・stub = False
    ・open_client = True
    ・pre_check = True
    ・necessity = ProcessStatus.show_or_unknown
    ・change_status = None
    ・post_check = False

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
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.show
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    open_client = True
    pre_check = True
    necessity = ProcessStatus.show_or_unknown
    change_status = None
    post_check = False

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.need_not_to_change

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00339, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00340, add_info:{[nf_name, 'process status: need_not_to_change']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=open_client)
    test_mocker.pre_check = mocker.Mock(return_value=pre_check)
    test_mocker.change_status = mocker.Mock(return_value=change_status)
    test_mocker.post_check = mocker.Mock(return_value=post_check)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.necessity = necessity
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


def test_run03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_run03 run試験03 異常系試験 (OK, mode:Mode.show, SSH接続異常)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.show
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    ・stub = False
    ・open_client = False
    ・pre_check = False
    ・necessity = 0
    ・change_status = None
    ・post_check = False

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
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.show
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    open_client = False
    pre_check = False
    necessity = 0
    change_status = None
    post_check = False

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.ssh_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00339, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00340, add_info:{[nf_name, 'process status: ssh_ng']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=open_client)
    test_mocker.pre_check = mocker.Mock(return_value=pre_check)
    test_mocker.change_status = mocker.Mock(return_value=change_status)
    test_mocker.post_check = mocker.Mock(return_value=post_check)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.necessity = necessity
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


def test_run04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_run04 run試験04 異常系試験 (OK, mode:Mode.show, PreCheck異常)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.show
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    ・stub = False
    ・open_client = True
    ・pre_check = False
    ・necessity = 0
    ・change_status = None
    ・post_check = False

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
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.show
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    open_client = True
    pre_check = False
    necessity = 0
    change_status = None
    post_check = False

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.pre_check_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00339, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00340, add_info:{[nf_name, 'process status: pre_check_ng']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=open_client)
    test_mocker.pre_check = mocker.Mock(return_value=pre_check)
    test_mocker.change_status = mocker.Mock(return_value=change_status)
    test_mocker.post_check = mocker.Mock(return_value=post_check)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.necessity = necessity

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


def test_run05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_run05 run試験05 異常系試験 (OK, mode:Mode.down, ChangeStatus異常:change_ng)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    ・stub = False
    ・open_client = True
    ・pre_check = True
    ・necessity = ProcessStatus.need_to_change
    ・change_status = ProcessStatus.change_ng
    ・post_check = False

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
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    open_client = True
    pre_check = True
    necessity = ProcessStatus.need_to_change
    change_status = ProcessStatus.change_ng
    post_check = False

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.change_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00339, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00340, add_info:{[nf_name, 'process status: change_ng']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=open_client)
    test_mocker.pre_check = mocker.Mock(return_value=pre_check)
    test_mocker.change_status = mocker.Mock(return_value=change_status)
    test_mocker.post_check = mocker.Mock(return_value=post_check)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.necessity = necessity
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


def test_run06(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_run06 run試験06 異常系試験 (OK, mode:Mode.down, ChangeStatus異常:commit_ng)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    ・stub = False
    ・open_client = True
    ・pre_check = True
    ・necessity = ProcessStatus.need_to_change
    ・change_status = ProcessStatus.commit_ng
    ・post_check = False

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
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    open_client = True
    pre_check = True
    necessity = ProcessStatus.need_to_change
    change_status = ProcessStatus.commit_ng
    post_check = False

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.change_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00339, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00340, add_info:{[nf_name, 'process status: change_ng']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=open_client)
    test_mocker.pre_check = mocker.Mock(return_value=pre_check)
    test_mocker.change_status = mocker.Mock(return_value=change_status)
    test_mocker.post_check = mocker.Mock(return_value=post_check)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.necessity = necessity
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
    """test_run07 run試験07 異常系試験 (OK, mode:Mode.down, PostCheck異常)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    ・stub = False
    ・open_client = True
    ・pre_check = True
    ・necessity = ProcessStatus.need_to_change
    ・change_status = ProcessStatus.commit_ok
    ・post_check = False

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
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    open_client = True
    pre_check = True
    necessity = ProcessStatus.need_to_change
    change_status = ProcessStatus.commit_ok
    post_check = False

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.post_check_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00339, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00340, add_info:{[nf_name, 'process status: post_check_ng']}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=open_client)
    test_mocker.pre_check = mocker.Mock(return_value=pre_check)
    test_mocker.change_status = mocker.Mock(return_value=change_status)
    test_mocker.post_check = mocker.Mock(return_value=post_check)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.necessity = necessity
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
    """test_run08 run試験08 異常系試験 (OK, mode:Mode.down, Exception発生)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・nf_name = "a2-er-s01-smfvo-001"
    ・mode = Mode.down
    ・edns_ipaddr = "2001:268:200d:1010::6"
    ・ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    ・stub = False
    ・open_client = True
    ・pre_check = Exception("Test Exception")
    ・necessity = ProcessStatus.need_to_change
    ・change_status = None
    ・post_check = False

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
    edns_name = "tys1tb1edns02"
    nf_name = "a2-er-s01-smfvo-001"
    mode = Mode.down
    edns_ipaddr = "2001:268:200d:1010::6"
    ipaddr_list = [
        "2001:268:200d:1010::6",
        "2001:268:200d:5010::6",
        "2001:268:200d:500f::6"
    ]
    stub = False
    open_client = True
    pre_check = Exception("Test Exception")
    necessity = ProcessStatus.need_to_change
    change_status = None
    post_check = False

    send_command = []

    command_response_value = []

    expected_value = ProcessStatus.exception_ng

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00339, add_info:{nf_name}\n",
        f"job_id:{JOB_ID}, message_id:I00340, add_info:{[nf_name, 'process status: exception_ng']}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:xCAP ipaddr変更プロセス異常:\n",
        f"パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" STATUS: {ProcessStatus.exception_ng.name}\n",
        f" Trace: Exception Test Exception\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_eri_process.NFShellClient", new=ClientForTest)
    mocker.patch("src.abc_eri_process.StubClient", new=StubClientForTest)

    test_mocker = mocker.MagicMock()
    test_mocker.sleep = mocker.Mock(return_value=True)
    test_mocker.open_client = mocker.Mock(return_value=open_client)
    test_mocker.pre_check = mocker.Mock(side_effect=pre_check)
    test_mocker.change_status = mocker.Mock(return_value=change_status)
    test_mocker.post_check = mocker.Mock(return_value=post_check)
    test_mocker.close_client = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    process = EriSmfvoXCAPProcess(edns_name, nf_name, mode, edns_ipaddr, ipaddr_list, stub, JOB_ID)
    process._AbcEricssonProcess__client = test_mocker
    process._AbcProcess__logger = logger
    process.necessity = necessity
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
