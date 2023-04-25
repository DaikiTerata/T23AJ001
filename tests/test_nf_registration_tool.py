from copy import deepcopy
import json
import pathlib
from typing import Any, List
import pytest
from pytest_mock import MockerFixture
from datetime import datetime

from xgnlog.Log import Level
from src.abc_process import ProcessStatus

from src.xcap_common import MODE_UNKNOWN, NF_NONE, Mode
import src.xcap_tool as target

JOB_ID = "T22AJ001"


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


class MockProcess:
    def __init__(self, edns_host: str, nf_name: str, mode: Mode, stub: bool):
        pass

    def run(self):
        pass


def test_Result01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_Result01 Result試験01 Enum取得

    試験条件
    ・status = Result.ok
    ・value = "OK"

    試験結果
    ・値が取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    status = target.Result.ok
    value = target.Result.ok.value

    expected_value = value

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.abc_registration_process.LOGGER", new=logger)

    response_value = str(status)

    assert response_value == expected_value


def test_check_args01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_args01 check_args試験01 正常試験 (mode: LIST, node: なし)

    試験条件
    ・コマンド引数
        ・script_name = "nf_registration_tool.py"
        ・mode = Mode.list

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "nf_registration_tool.py"
    nf_name = "b1-CPA_East-Act"
    mode = Mode.list
    blocked_nf = ""
    batch = False
    stub = False
    argv = [script_name, mode.value]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = True

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00103", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00104", [NF_NONE] + argv[1:])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    tool = target.NfRegistrationTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert tool.args.nf_name is not None
    assert tool.args.nf_name == NF_NONE
    assert tool.args.mode is not None
    assert tool.args.mode == mode
    assert tool.args.blocked_nflist is not None
    assert tool.args.blocked_nflist == blocked_nflist
    assert tool.args.batch is not None
    assert tool.args.batch == batch
    assert tool.args.stub is not None
    assert tool.args.stub == stub
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_args02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_args02 check_args試験02 正常試験 (mode: LIST, node: あり)

    試験条件
    ・コマンド引数
        ・script_name = "nf_registration_tool.py"
        ・nf_name = "b1-CPA_East-Act"
        ・mode = Mode.list
        ・blocked_node = ""
        ・batch = False
        ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "nf_registration_tool.py"
    nf_name = "b1-CPA_East-Act"
    mode = Mode.list
    blocked_nf = ""
    batch = False
    stub = False
    argv = [script_name, nf_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = True

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00103", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00104", argv[1:])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    tool = target.NfRegistrationTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert tool.args.nf_name is not None
    assert tool.args.nf_name == nf_name
    assert tool.args.mode is not None
    assert tool.args.mode == mode
    assert tool.args.blocked_nflist is not None
    assert tool.args.blocked_nflist == blocked_nflist
    assert tool.args.batch is not None
    assert tool.args.batch == batch
    assert tool.args.stub is not None
    assert tool.args.stub == stub
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_args03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_args03 check_args試験03 正常試験 (mode: INFO)

    試験条件
    ・コマンド引数
        ・script_name = "nf_registration_tool.py"
        ・nf_name = "b1-CPA_East-Act"
        ・mode = Mode.info
        ・blocked_node = ""
        ・batch = False
        ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "nf_registration_tool.py"
    nf_name = "b1-CPA_East-Act"
    mode = Mode.info
    blocked_nf = ""
    batch = False
    stub = False
    argv = [script_name, nf_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = True

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00103", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00104", argv[1:])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    tool = target.NfRegistrationTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert tool.args.nf_name is not None
    assert tool.args.nf_name == nf_name
    assert tool.args.mode is not None
    assert tool.args.mode == mode
    assert tool.args.blocked_nflist is not None
    assert tool.args.blocked_nflist == blocked_nflist
    assert tool.args.batch is not None
    assert tool.args.batch == batch
    assert tool.args.stub is not None
    assert tool.args.stub == stub
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_args04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_args04 check_args試験04 正常試験 (mode: SHOW)

    試験条件
    ・コマンド引数
        ・script_name = "nf_registration_tool.py"
        ・nf_name = "b1-CPA_East-Act"
        ・mode = Mode.show
        ・blocked_node = ""
        ・batch = False
        ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "nf_registration_tool.py"
    nf_name = "b1-CPA_East-Act"
    mode = Mode.show
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = False
    stub = False
    argv = [script_name, nf_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = True

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00103", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00104", argv[1:])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    tool = target.NfRegistrationTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert tool.args.nf_name is not None
    assert tool.args.nf_name == nf_name
    assert tool.args.mode is not None
    assert tool.args.mode == mode
    assert tool.args.blocked_nflist is not None
    assert tool.args.blocked_nflist == blocked_nflist
    assert tool.args.batch is not None
    assert tool.args.batch == batch
    assert tool.args.stub is not None
    assert tool.args.stub == stub
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_args05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_args05 check_args試験05 正常試験 (mode: UP)

    試験条件
    ・コマンド引数
        ・script_name = "nf_registration_tool.py"
        ・nf_name = "b1-CPA_East-Act"
        ・mode = Mode.up
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = False
        ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "nf_registration_tool.py"
    nf_name = "b1-CPA_East-Act"
    mode = Mode.up
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = False
    stub = False
    argv = [script_name, nf_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = True

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00103", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00104", argv[1:])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    tool = target.NfRegistrationTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert tool.args.nf_name is not None
    assert tool.args.nf_name == nf_name
    assert tool.args.mode is not None
    assert tool.args.mode == mode
    assert tool.args.blocked_nflist is not None
    assert tool.args.blocked_nflist == blocked_nflist
    assert tool.args.batch is not None
    assert tool.args.batch == batch
    assert tool.args.stub is not None
    assert tool.args.stub == stub
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_args06(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_args06 check_args試験06 正常試験 (mode: DOWN)

    試験条件
    ・コマンド引数
        ・script_name = "nf_registration_tool.py"
        ・nf_name = "b1-CPA_East-Act"
        ・mode = Mode.down
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = False
        ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "nf_registration_tool.py"
    nf_name = "b1-CPA_East-Act"
    mode = Mode.down
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = False
    stub = False
    argv = [script_name, nf_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = True

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00103", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00104", argv[1:])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    tool = target.NfRegistrationTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert tool.args.nf_name is not None
    assert tool.args.nf_name == nf_name
    assert tool.args.mode is not None
    assert tool.args.mode == mode
    assert tool.args.blocked_nflist is not None
    assert tool.args.blocked_nflist == blocked_nflist
    assert tool.args.batch is not None
    assert tool.args.batch == batch
    assert tool.args.stub is not None
    assert tool.args.stub == stub
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_args07(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_args07 check_args試験07 正常試験 (mode: UP, batch: True)

    試験条件
    ・コマンド引数
        ・script_name = "nf_registration_tool.py"
        ・nf_name = "b1-CPA_East-Act"
        ・mode = Mode.up
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = True
        ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がNoneであること
    ・各コマンド引数が正常に取得できること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "nf_registration_tool.py"
    nf_name = "b1-CPA_East-Act"
    mode = Mode.up
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = True
    stub = False
    argv = [script_name, nf_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = True

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00103", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00104", argv[1:])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    tool = target.NfRegistrationTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert tool.args.nf_name is not None
    assert tool.args.nf_name == nf_name
    assert tool.args.mode is not None
    assert tool.args.mode == mode
    assert tool.args.blocked_nflist is not None
    assert tool.args.blocked_nflist == blocked_nflist
    assert tool.args.batch is not None
    assert tool.args.batch == batch
    assert tool.args.stub is not None
    assert tool.args.stub == stub
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_args08(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_args08 check_args試験08 正常試験 (mode: DOWN, stub:True)

    試験条件
    ・コマンド引数
        ・script_name = "nf_registration_tool.py"
        ・nf_name = "b1-CPA_East-Act"
        ・mode = Mode.down
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = False
        ・stub = True

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "nf_registration_tool.py"
    nf_name = "b1-CPA_East-Act"
    mode = Mode.down
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = False
    stub = True
    argv = [script_name, nf_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = True

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00103", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00104", argv[1:])
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    tool = target.NfRegistrationTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert tool.args.nf_name is not None
    assert tool.args.nf_name == nf_name
    assert tool.args.mode is not None
    assert tool.args.mode == mode
    assert tool.args.blocked_nflist is not None
    assert tool.args.blocked_nflist == blocked_nflist
    assert tool.args.batch is not None
    assert tool.args.batch == batch
    assert tool.args.stub is not None
    assert tool.args.stub == stub
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_args09(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_args09 check_args試験09 異常系試験 (nf_name: なし)

    試験条件
    ・コマンド引数
        ・script_name = "nf_registration_tool.py"
        ・nf_name = ""
        ・mode = Mode.down
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = False
        ・stub = True

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    script_name = "pcscf_service_tool.py"
    nf_name = ""
    mode = Mode.show
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = False
    stub = False
    argv = [script_name, nf_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = False
    tool_expected_value = "NG"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):failed to analyse arguments {0}.\n".format(argv[1:], mode=MODE_UNKNOWN, time=logtime_str, edns_host=NF_NONE, nf_name=NF_NONE),
        "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]\n".format(tool_expected_value, mode=MODE_UNKNOWN, time=logtime_str, edns_host=NF_NONE, nf_name=NF_NONE),
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00103", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00102", argv[1:])
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:引数解析異常発生:\n",
        "パラメータ:\n",
        f" 引数: {argv[1:]}\n",
        " Trace: ArgumentParserError Argument is None, null string or blank only.\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    response_value = tool.check_args()

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


def test_check_args10(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_check_args10 check_args試験10 異常系試験 (mode: なし)

    試験条件
    ・コマンド引数
        ・script_name = "nf_registration_tool.py"
        ・nf_name = "b1-CPA_East-Act"
        ・mode = ""
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = False
        ・stub = True

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    script_name = "pcscf_service_tool.py"
    nf_name = "b1-CPA_East-Act"
    mode = ""
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = False
    stub = False
    argv = [script_name, nf_name, mode, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = False
    tool_expected_value = "NG"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):failed to analyse arguments {0}.\n".format(argv[1:], mode=MODE_UNKNOWN, time=logtime_str, edns_host=NF_NONE, nf_name=NF_NONE),
        "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]\n".format(tool_expected_value, mode=MODE_UNKNOWN, time=logtime_str, edns_host=NF_NONE, nf_name=NF_NONE),
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00103", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00102", argv[1:])
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:引数解析異常発生:\n",
        "パラメータ:\n",
        f" 引数: {argv[1:]}\n",
        " Trace: ArgumentParserError argument mode: invalid Mode value: ''\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    response_value = tool.check_args()

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


CONF_TOOL = pathlib.Path("config").joinpath("nf-registration-tool.json")
CONF_MODULES = pathlib.Path("config").joinpath("nf-modules.json")
CONF_INFOS = pathlib.Path("config").joinpath("nf-infos.json")
CONF_edns_host = pathlib.Path("config").joinpath("nf-edns_host.json")
with open(CONF_TOOL, "r", encoding="utf-8") as f:
    DICT_TOOL = json.load(f)
with open(CONF_MODULES, "r", encoding="utf-8") as f:
    DICT_MODULES = json.load(f)
with open(CONF_INFOS, "r", encoding="utf-8") as f:
    DICT_INFOS = json.load(f)
with open(CONF_edns_host, "r", encoding="utf-8") as f:
    DICT_edns_host = json.load(f)


def test_load_config01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_load_config01 load_config試験01 正常系試験

    試験条件
    ・全設定ファイルを指定

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・json_check_and_loadが4回呼ばれること
    ・json_check_and_loadの引数がそれぞれ、CONF_TOOL,CONF_MODULES,CONF_TYPE,CONF_edns_hostであること
    ・tool_confが想定しているdictであること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    tool_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-registration-tool.json")
    module_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-modules.json")
    type_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-infos.json")
    edns_host_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-edns_host.json")

    tool_dict_expected_value = deepcopy(DICT_TOOL)
    tool_dict_expected_value["nf_modules"] = DICT_MODULES
    tool_dict_expected_value["nf_infos"] = DICT_INFOS
    tool_dict_expected_value["nf_edns_host"] = DICT_edns_host

    edns_host = "b1-CPA_East-Act"
    nf_name = "b1-CPA_East-Act"
    mode = Mode.up

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00105", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00106", None)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.json_check_and_load = mocker.Mock(side_effect=[deepcopy(DICT_TOOL), DICT_MODULES, DICT_INFOS, DICT_edns_host])
    mocker.patch("src.nf_registration_tool.json_check_and_load", test_mocker.json_check_and_load)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.load_config()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.json_check_and_load.called == True
    assert test_mocker.json_check_and_load.call_count == 4
    assert test_mocker.json_check_and_load.call_args_list[0][0] == (tool_conf_path, ("nf_modules", "nf_infos", "nf_edns_host"))
    assert test_mocker.json_check_and_load.call_args_list[1][0] == (module_conf_path,)
    assert test_mocker.json_check_and_load.call_args_list[2][0] == (type_conf_path,)
    assert test_mocker.json_check_and_load.call_args_list[3][0] == (edns_host_conf_path,)
    assert tool.tool_conf == tool_dict_expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_load_config02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_load_config02 load_config試験02 異常系試験 (ファイルなし)

    試験条件
    ・全設定ファイルを指定

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseであること
    ・json_check_and_loadが4回呼ばれること
    ・json_check_and_loadの引数がそれぞれ、CONF_TOOL,CONF_MODULES,CONF_TYPE,CONF_edns_hostであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    tool_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-registration-tool.json")
    module_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-modules.json")
    type_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-infos.json")
    edns_host_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-edns_host.json")

    edns_host = "b1-CPA_East-Act"
    nf_name = "b1-CPA_East-Act"
    mode = Mode.down

    expected_value = False
    tool_expected_value = "NG"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):configuration files not found. file={0}\n".format(edns_host_conf_path, mode=mode, time=logtime_str, edns_host=edns_host, nf_name=NF_NONE),
        "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]\n".format(tool_expected_value, mode=mode, time=logtime_str, edns_host=edns_host, nf_name=NF_NONE)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00105", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00103", edns_host_conf_path)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:設定ファイルなし発生:\n",
        "パラメータ:\n",
        f" ファイルパス: {edns_host_conf_path}\n",
        f" Trace: FileNotFoundError File Not Found\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.json_check_and_load = mocker.Mock(side_effect=[deepcopy(DICT_TOOL), DICT_MODULES, DICT_INFOS, FileNotFoundError("File Not Found")])
    mocker.patch("src.nf_registration_tool.json_check_and_load", test_mocker.json_check_and_load)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.load_config()

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
    assert test_mocker.json_check_and_load.called == True
    assert test_mocker.json_check_and_load.call_count == 4
    assert test_mocker.json_check_and_load.call_args_list[0][0] == (tool_conf_path, ("nf_modules", "nf_infos", "nf_edns_host"))
    assert test_mocker.json_check_and_load.call_args_list[1][0] == (module_conf_path,)
    assert test_mocker.json_check_and_load.call_args_list[2][0] == (type_conf_path,)
    assert test_mocker.json_check_and_load.call_args_list[3][0] == (edns_host_conf_path,)
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_load_config03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_load_config03 load_config試験03 異常系試験 (JSON解析エラー)

    試験条件
    ・全設定ファイルを指定

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseであること
    ・json_check_and_loadが4回呼ばれること
    ・json_check_and_loadの引数がそれぞれ、CONF_TOOL,CONF_MODULES,CONF_TYPE,CONF_edns_hostであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    tool_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-registration-tool.json")
    module_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-modules.json")
    type_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-infos.json")
    edns_host_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-edns_host.json")

    edns_host = "b1-CPA_East-Act"
    nf_name = "b1-CPA_East-Act"
    mode = Mode.down

    expected_value = False
    tool_expected_value = "NG"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):failed to analyse configuration files. file={0}\n".format(edns_host_conf_path, mode=mode, time=logtime_str, edns_host=edns_host, nf_name=NF_NONE),
        "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]\n".format(tool_expected_value, mode=mode, time=logtime_str, edns_host=edns_host, nf_name=NF_NONE)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00105", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00103", edns_host_conf_path)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:設定ファイルJSON異常発生:\n",
        "パラメータ:\n",
        f" ファイルパス: {edns_host_conf_path}\n",
        f" Trace: JSONDecodeError filename: line 1 column 2 (char 1)\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.json_check_and_load = mocker.Mock(side_effect=[deepcopy(DICT_TOOL), DICT_MODULES, DICT_INFOS, json.JSONDecodeError("filename", "test", 1)])
    mocker.patch("src.nf_registration_tool.json_check_and_load", test_mocker.json_check_and_load)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.load_config()

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
    assert test_mocker.json_check_and_load.called == True
    assert test_mocker.json_check_and_load.call_count == 4
    assert test_mocker.json_check_and_load.call_args_list[0][0] == (tool_conf_path, ("nf_modules", "nf_infos", "nf_edns_host"))
    assert test_mocker.json_check_and_load.call_args_list[1][0] == (module_conf_path,)
    assert test_mocker.json_check_and_load.call_args_list[2][0] == (type_conf_path,)
    assert test_mocker.json_check_and_load.call_args_list[3][0] == (edns_host_conf_path,)
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_load_config04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_load_config04 load_config試験04 異常系試験 (必須キーなし)

    試験条件
    ・全設定ファイルを指定

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseであること
    ・json_check_and_loadが4回呼ばれること
    ・json_check_and_loadの引数がそれぞれ、CONF_TOOL,CONF_MODULES,CONF_TYPE,CONF_edns_hostであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    tool_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-registration-tool.json")
    module_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-modules.json")
    type_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-infos.json")
    edns_host_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "nf-edns_host.json")

    edns_host = "b1-CPA_East-Act"
    nf_name = "b1-CPA_East-Act"
    mode = Mode.down

    expected_value = False
    tool_expected_value = "NG"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):required json key not found. file={0}, key={1}\n".format(edns_host_conf_path, "nf_edns_host", mode=mode, time=logtime_str, edns_host=edns_host, nf_name=NF_NONE),
        "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]\n".format(tool_expected_value, mode=mode, time=logtime_str, edns_host=edns_host, nf_name=NF_NONE)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00105", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00103", edns_host_conf_path)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:設定ファイル必須キーなし発生:\n",
        "パラメータ:\n",
        f" ファイルパス: {edns_host_conf_path}\n",
        f" Trace: KeyError 'Key Error'\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.json_check_and_load = mocker.Mock(side_effect=[deepcopy(DICT_TOOL), DICT_MODULES, DICT_INFOS, KeyError("Key Error")])
    mocker.patch("src.nf_registration_tool.json_check_and_load", test_mocker.json_check_and_load)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.load_config()

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
    assert test_mocker.json_check_and_load.called == True
    assert test_mocker.json_check_and_load.call_count == 4
    assert test_mocker.json_check_and_load.call_args_list[0][0] == (tool_conf_path, ("nf_modules", "nf_infos", "nf_edns_host"))
    assert test_mocker.json_check_and_load.call_args_list[1][0] == (module_conf_path,)
    assert test_mocker.json_check_and_load.call_args_list[2][0] == (type_conf_path,)
    assert test_mocker.json_check_and_load.call_args_list[3][0] == (edns_host_conf_path,)
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_info01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_info01 info試験01 正常試験 (OK)

    試験条件
    ・コマンド引数
        ・script_name = "nf_registration_tool.py"
        ・edns_host = "b1-CPA_East-Act"
        ・nf_name = ["a2-er-s01-smfent-001"]
        ・mode = Mode.up
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = True
        ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "nf_registration_tool.py"
    nf_name = "b1-CPA_East-Act"
    edns_host = nf_name
    nf_name_list = ["a2-er-s01-smfent-001"]
    mode = Mode.up
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = True
    stub = False
    blocked_nflist = blocked_nf.split(",")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = None

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"     edns_host: b1-CPA_East-Act\n",
        f"        NF: ['a2-er-s01-smfent-001']\n",
        f"      MODE: UP\n",
        f"   COMMENT: nf status to registered\n",
        f"BLOCKED NF: a1-er-s01-amf-001\n",
        f"            a2-er-s01-smfvo-001\n",
        f"     BATCH: True\n",
        f"\n",
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00107", None),
        *"job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00108", "".join(expected_sout[:-1])).splitlines(True)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name_list = nf_name_list
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.info()

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


def test_get_nf_module_info01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_nf_module_info01 get_nf_module_info試験01 正常系試験 (OK)

    試験条件
    ・全設定ファイルを指定
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "b1-er-s02-smfent-001"
    ・mode = Mode.up

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果が(nf_type, module_name, class_name)であること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_modules"] = DICT_MODULES
    tool_dict["nf_infos"] = DICT_INFOS

    edns_host = "b1-CPA_East-Act"
    nf_name = "b1-er-s02-smfent-001"
    mode = Mode.up

    nf_type = "smfent"
    module_name = "src.eri_smf_registration_process"
    class_name = "EriSmfRegistrationProcess"

    expected_value = (nf_type, module_name, class_name)

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00109", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00110", expected_value)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.mode = mode

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.get_nf_module_info(nf_name)

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


def test_get_nf_module_info02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_nf_module_info02 get_nf_module_info試験02 異常系試験 (対象NFなし)

    試験条件
    ・全設定ファイルを指定
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "NO_NF"
    ・mode = Mode.up

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果が(None, None, None)であること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_modules"] = DICT_MODULES
    tool_dict["nf_infos"] = DICT_INFOS

    edns_host = "b1-CPA_East-Act"
    nf_name = "NO_NF"
    mode = Mode.up

    nf_type = None
    module_name = None
    class_name = None

    expected_value = (nf_type, module_name, class_name)

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):nf configuration not found.\n".format(mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00109", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "E00104", edns_host)
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:NFツール設定取得失敗:\n",
        "パラメータ:\n",
        f" NF名: {nf_name}\n",
        f" Trace: KeyError 'NO_NF'\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.mode = mode

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.get_nf_module_info(nf_name)

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


def test_get_main01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_main01 main試験01 正常系試験 (LISTモード)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "b1-CPA_East-Act"
    ・mode = Mode.list
    ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    ・batch = False
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_modules"] = DICT_MODULES
    tool_dict["nf_infos"] = DICT_INFOS
    tool_dict["nf_edns_host"] = DICT_edns_host

    nf_name = "b1-CPA_East-Act"
    edns_host = nf_name
    mode = Mode.list
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    blocked_nflist = blocked_nf.split(",")
    batch = False
    stub = False

    nf_list = [
        "a1-er-s01-smf-001",
        "a1-er-s01-smfvo-001",
        "a2-er-s01-smf-001",
        "a2-er-s01-smfvo-001",
        "a2-er-s01-smfsl-001",
        "a2-er-s01-smfent-001",
        "a2-er-s01-smfvoroout-001",
        "a2-er-s02-smf-001",
        "a2-er-s02-smfvo-001",
        "a2-er-s02-smfsl-001",
        "a2-er-s02-smfent-001",
        "b1-er-s01-smf-001",
        "b1-er-s01-smfvo-001",
        "b1-er-s01-smfsl-001",
        "b1-er-s01-smfent-001",
        "b1-er-s01-smfvoroout-001",
        "b1-er-s02-smf-001",
        "b1-er-s02-smfvo-001",
        "b1-er-s02-smfsl-001",
        "b1-er-s02-smfent-001",
    ]

    edns_host_list = [
        "b1-CPA_East-Act",
        "a2-CPA_East-Sby",
        "osc2-CPA_West-Act",
        "tam5-CPA_West-Sby",
        "tam5-CPA_East-Act",
        "osc2-CPA_East-Sby"
    ]

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "==NF LIST==\n",
        *[f" {x}\n" for x in nf_list],
        "\n",
        "==edns_host LIST==\n",
        *[f" {x}\n" for x in edns_host_list]
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00111", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00113", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00114", [nf_list, edns_host_list]),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00112", None),
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.main()

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


def test_get_main02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_main02 main試験02 正常系試験 (INFOモード)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "b1-CPA_East-Act"
    ・mode = Mode.info
    ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    ・batch = False
    ・stub = True

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_modules"] = DICT_MODULES
    tool_dict["nf_infos"] = DICT_INFOS
    tool_dict["nf_edns_host"] = DICT_edns_host

    nf_name = "b1-CPA_East-Act"
    edns_host = nf_name
    mode = Mode.info
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    blocked_nflist = blocked_nf.split(",")
    batch = False
    stub = True

    tool_expected_value = "OK"

    nf_type = "smfent"
    module_name = "src.eri_smf_registration_process"
    class_name = "EriSmfRegistrationProcess"
    module_info = (nf_type, module_name, class_name)

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "===== STUB MODE [ ON ] =====\n",
        "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]\n".format(tool_expected_value, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00111", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00120", tool_expected_value),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00112", None),
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_nf_module_info = mocker.Mock(return_value=module_info)
    test_mocker.info = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_nf_module_info", test_mocker.get_nf_module_info)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

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


def test_get_main03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_main03 main試験03 正常系試験 (UPモード, interactive: "n")

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "b1-CPA_East-Act"
    ・mode = Mode.up
    ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    ・batch = False
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_modules"] = DICT_MODULES
    tool_dict["nf_infos"] = DICT_INFOS
    tool_dict["nf_edns_host"] = DICT_edns_host

    nf_name = "b1-CPA_East-Act"
    edns_host = nf_name
    mode = Mode.up
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    blocked_nflist = blocked_nf.split(",")
    batch = False
    stub = False

    tool_expected_value = "OK"

    nf_type = "smfent"
    module_name = "src.eri_smf_registration_process"
    class_name = "EriSmfRegistrationProcess"
    module_info = (nf_type, module_name, class_name)

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[INFO]:{mode}:{time}:{edns_host}({nf_name}):script was aborted due to an interractive action.\n".format(mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00111", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00121", "n"),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00112", None),
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_nf_module_info = mocker.Mock(return_value=module_info)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.interactive_check = mocker.Mock(return_value=(False, "n"))

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)
    mocker.patch("src.nf_registration_tool.interactive_check", test_mocker.interactive_check)

    tool = target.NfRegistrationTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_nf_module_info", test_mocker.get_nf_module_info)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

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


def test_get_main04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_main04 main試験04 正常系試験 (UPモード, エイリアス)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "b1-CPA_East-Act"
    ・mode = Mode.up
    ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    ・batch = True
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_modules"] = DICT_MODULES
    tool_dict["nf_infos"] = DICT_INFOS
    tool_dict["nf_edns_host"] = DICT_edns_host

    nf_name = "b1-CPA_East-Act"
    edns_host = nf_name
    mode = Mode.up
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    blocked_nflist = blocked_nf.split(",")
    batch = True
    stub = False

    expected_success_list = ["a2-er-s01-smfent-001"]
    expected_failed_list = []
    expected_blocked_list = []
    tool_expected_value = "OK"

    nf_type = "smfent"
    module_name = "src.eri_smf_registration_process"
    class_name = "EriSmfRegistrationProcess"
    module_info = (nf_type, module_name, class_name)

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "Start Time: {}\n".format(logtime_str),
        "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]\n".format(tool_expected_value, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):SUCCESS={0}, FAILED={1}, BLOCKED={2}\n".format(len(expected_success_list), len(expected_failed_list), len(expected_blocked_list), mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of FAILED NF={0}, FAILED NF {1}\n".format(len(expected_failed_list), expected_failed_list, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of BLOCKED NF={0}, BLOCKED NF {1}\n".format(len(expected_blocked_list), expected_blocked_list, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "End Time: {}\n".format(logtime_str)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00111", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00115", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00116", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00117", expected_success_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00118", expected_failed_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00119", expected_blocked_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00120", tool_expected_value),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00112", None),
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_nf_module_info = mocker.Mock(return_value=module_info)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.import_module = mocker.Mock(return_value=None)
    test_mocker.getattr = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.post_check_ok)
    mocker.patch("src.nf_registration_tool.import_module", test_mocker.import_module)
    mocker.patch("src.nf_registration_tool.getattr", test_mocker.getattr)
    mocker.patch("tests.test_nf_registration_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)
    mocker.patch("src.nf_registration_tool.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_nf_module_info", test_mocker.get_nf_module_info)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

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


def test_get_main05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_main05 main試験05 正常系試験 (UPモード, nf_name)

    試験条件
    ・edns_host = "b1-er-s02-smfent-001"
    ・nf_name = "b1-er-s02-smfent-001"
    ・mode = Mode.up
    ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    ・batch = True
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_modules"] = DICT_MODULES
    tool_dict["nf_infos"] = DICT_INFOS
    tool_dict["nf_edns_host"] = DICT_edns_host

    nf_name = "b1-er-s02-smfent-001"
    edns_host = nf_name
    mode = Mode.up
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    blocked_nflist = blocked_nf.split(",")
    batch = True
    stub = False

    expected_success_list = ["b1-er-s02-smfent-001"]
    expected_failed_list = []
    expected_blocked_list = []
    tool_expected_value = "OK"

    nf_type = "smfent"
    module_name = "src.eri_smf_registration_process"
    class_name = "EriSmfRegistrationProcess"
    module_info = (nf_type, module_name, class_name)

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "Start Time: {}\n".format(logtime_str),
        "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]\n".format(tool_expected_value, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):SUCCESS={0}, FAILED={1}, BLOCKED={2}\n".format(len(expected_success_list), len(expected_failed_list), len(expected_blocked_list), mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of FAILED NF={0}, FAILED NF {1}\n".format(len(expected_failed_list), expected_failed_list, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of BLOCKED NF={0}, BLOCKED NF {1}\n".format(len(expected_blocked_list), expected_blocked_list, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "End Time: {}\n".format(logtime_str)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00111", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00115", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00116", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00117", expected_success_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00118", expected_failed_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00119", expected_blocked_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00120", tool_expected_value),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00112", None),
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_nf_module_info = mocker.Mock(return_value=module_info)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.import_module = mocker.Mock(return_value=None)
    test_mocker.getattr = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.need_not_to_change)
    mocker.patch("src.nf_registration_tool.import_module", test_mocker.import_module)
    mocker.patch("src.nf_registration_tool.getattr", test_mocker.getattr)
    mocker.patch("tests.test_nf_registration_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)
    mocker.patch("src.nf_registration_tool.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_nf_module_info", test_mocker.get_nf_module_info)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

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


def test_get_main06(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_main06 main試験06 準正常系試験 (UPモード, プロセスNG, プロセス失敗)

    試験条件
    ・edns_host = "b1-er-s02-smfent-001"
    ・nf_name = "b1-er-s02-smfent-001"
    ・mode = Mode.up
    ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    ・batch = True
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_modules"] = DICT_MODULES
    tool_dict["nf_infos"] = DICT_INFOS
    tool_dict["nf_edns_host"] = DICT_edns_host

    nf_name = "b1-er-s02-smfent-001"
    edns_host = nf_name
    mode = Mode.up
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    blocked_nflist = blocked_nf.split(",")
    batch = True
    stub = False

    expected_success_list = []
    expected_failed_list = ["b1-er-s02-smfent-001"]
    expected_blocked_list = []
    tool_expected_value = "NG"

    nf_type = "smfent"
    module_name = "src.eri_smf_registration_process"
    class_name = "EriSmfRegistrationProcess"
    module_info = (nf_type, module_name, class_name)

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "Start Time: {}\n".format(logtime_str),
        "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]\n".format(tool_expected_value, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):SUCCESS={0}, FAILED={1}, BLOCKED={2}\n".format(len(expected_success_list), len(expected_failed_list), len(expected_blocked_list), mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of FAILED NF={0}, FAILED NF {1}\n".format(len(expected_failed_list), expected_failed_list, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of BLOCKED NF={0}, BLOCKED NF {1}\n".format(len(expected_blocked_list), expected_blocked_list, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "End Time: {}\n".format(logtime_str)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00111", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00115", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00116", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00117", expected_success_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00118", expected_failed_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00119", expected_blocked_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00120", tool_expected_value),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00112", None),
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_nf_module_info = mocker.Mock(return_value=module_info)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.import_module = mocker.Mock(return_value=None)
    test_mocker.getattr = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.change_ng)
    mocker.patch("src.nf_registration_tool.import_module", test_mocker.import_module)
    mocker.patch("src.nf_registration_tool.getattr", test_mocker.getattr)
    mocker.patch("tests.test_nf_registration_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)
    mocker.patch("src.nf_registration_tool.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_nf_module_info", test_mocker.get_nf_module_info)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

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


def test_get_main07(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_main07 main試験07 準正常系試験 (UPモード, プロセスNG, 閉塞中ノード)

    試験条件
    ・edns_host = "b1-er-s02-smfent-001"
    ・nf_name = "b1-er-s02-smfent-001"
    ・mode = Mode.up
    ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001,b1-er-s02-smfent-001"
    ・batch = True
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_modules"] = DICT_MODULES
    tool_dict["nf_infos"] = DICT_INFOS
    tool_dict["nf_edns_host"] = DICT_edns_host

    nf_name = "b1-er-s02-smfent-001"
    edns_host = nf_name
    mode = Mode.up
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001,b1-er-s02-smfent-001"
    blocked_nflist = blocked_nf.split(",")
    batch = True
    stub = False

    expected_success_list = []
    expected_failed_list = []
    expected_blocked_list = ["b1-er-s02-smfent-001"]
    tool_expected_value = "OK"

    nf_type = "smfent"
    module_name = "src.eri_smf_registration_process"
    class_name = "EriSmfRegistrationProcess"
    module_info = (nf_type, module_name, class_name)

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "Start Time: {}\n".format(logtime_str),
        "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]\n".format(tool_expected_value, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):SUCCESS={0}, FAILED={1}, BLOCKED={2}\n".format(len(expected_success_list), len(expected_failed_list), len(expected_blocked_list), mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of FAILED NF={0}, FAILED NF {1}\n".format(len(expected_failed_list), expected_failed_list, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of BLOCKED NF={0}, BLOCKED NF {1}\n".format(len(expected_blocked_list), expected_blocked_list, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "End Time: {}\n".format(logtime_str)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00111", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00115", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00116", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00117", expected_success_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00118", expected_failed_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00119", expected_blocked_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00120", tool_expected_value),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00112", None),
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_nf_module_info = mocker.Mock(return_value=module_info)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.import_module = mocker.Mock(return_value=None)
    test_mocker.getattr = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.exception_ng)
    mocker.patch("src.nf_registration_tool.import_module", test_mocker.import_module)
    mocker.patch("src.nf_registration_tool.getattr", test_mocker.getattr)
    mocker.patch("tests.test_nf_registration_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)
    mocker.patch("src.nf_registration_tool.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_nf_module_info", test_mocker.get_nf_module_info)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

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


def test_get_main08(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_main08 main試験08 異常系試験 (UPモード, モジュール情報取得失敗)

    試験条件
    ・edns_host = "b1-er-s02-smfent-001"
    ・nf_name = "b1-er-s02-smfent-001"
    ・mode = Mode.up
    ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    ・batch = True
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_modules"] = DICT_MODULES
    tool_dict["nf_infos"] = DICT_INFOS
    tool_dict["nf_edns_host"] = DICT_edns_host

    nf_name = "b1-er-s02-smfent-001"
    edns_host = nf_name
    mode = Mode.up
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    blocked_nflist = blocked_nf.split(",")
    batch = True
    stub = False

    expected_success_list = []
    expected_failed_list = ["b1-er-s02-smfent-001"]
    expected_blocked_list = []
    tool_expected_value = "NG"

    nf_type = "smfent"
    module_name = "src.eri_smf_registration_process"
    class_name = "EriSmfRegistrationProcess"
    module_info = (None, None, None)

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]\n".format(tool_expected_value, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00111", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00120", tool_expected_value),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00112", None),
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_nf_module_info = mocker.Mock(return_value=module_info)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.import_module = mocker.Mock(return_value=None)
    test_mocker.getattr = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.exception_ng)
    mocker.patch("src.nf_registration_tool.import_module", test_mocker.import_module)
    mocker.patch("src.nf_registration_tool.getattr", test_mocker.getattr)
    mocker.patch("tests.test_nf_registration_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)
    mocker.patch("src.nf_registration_tool.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_nf_module_info", test_mocker.get_nf_module_info)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

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


def test_get_main09(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_main09 main試験09 正常系試験 (UPモード, エイリアス, nf_name_list: 2nf)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "b1-CPA_East-Act"
    ・nf_name_list = ["a2-er-s01-smfent-001", "b1-er-s02-smfent-001"]
    ・mode = Mode.up
    ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    ・batch = True
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_modules"] = DICT_MODULES
    tool_dict["nf_infos"] = DICT_INFOS
    tool_dict["nf_edns_host"] = deepcopy(DICT_edns_host)

    nf_name = "b1-CPA_East-Act"
    edns_host = nf_name
    mode = Mode.up
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    blocked_nflist = blocked_nf.split(",")
    batch = True
    stub = False

    tool_dict["nf_edns_host"][edns_host] = ["a2-er-s01-smfent-001", "b1-er-s02-smfent-001"]

    expected_success_list = ["a2-er-s01-smfent-001", "b1-er-s02-smfent-001"]
    expected_failed_list = []
    expected_blocked_list = []
    tool_expected_value = "OK"

    nf_type = "smfent"
    module_name = "src.eri_smf_registration_process"
    class_name = "EriSmfRegistrationProcess"
    module_info = (nf_type, module_name, class_name)

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "Start Time: {}\n".format(logtime_str),
        "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]\n".format(tool_expected_value, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):SUCCESS={0}, FAILED={1}, BLOCKED={2}\n".format(len(expected_success_list), len(expected_failed_list), len(expected_blocked_list), mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of FAILED NF={0}, FAILED NF {1}\n".format(len(expected_failed_list), expected_failed_list, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of BLOCKED NF={0}, BLOCKED NF {1}\n".format(len(expected_blocked_list), expected_blocked_list, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "End Time: {}\n".format(logtime_str)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00111", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00115", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00116", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00117", expected_success_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00118", expected_failed_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00119", expected_blocked_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00120", tool_expected_value),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00112", None),
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_nf_module_info = mocker.Mock(return_value=module_info)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.import_module = mocker.Mock(return_value=None)
    test_mocker.getattr = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.post_check_ok)
    mocker.patch("src.nf_registration_tool.import_module", test_mocker.import_module)
    mocker.patch("src.nf_registration_tool.getattr", test_mocker.getattr)
    mocker.patch("tests.test_nf_registration_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)
    mocker.patch("src.nf_registration_tool.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_nf_module_info", test_mocker.get_nf_module_info)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

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


def test_get_main10(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_main10 main試験10 準正常系試験 (UPモード, エイリアス, nf_name_list: 2NF, 1NFプロセス失敗)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "b1-CPA_East-Act"
    ・nf_name_list = ["a2-er-s01-smfent-001", "b1-er-s02-smfent-001"]
    ・mode = Mode.up
    ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    ・batch = True
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_modules"] = DICT_MODULES
    tool_dict["nf_infos"] = DICT_INFOS
    tool_dict["nf_edns_host"] = deepcopy(DICT_edns_host)

    nf_name = "b1-CPA_East-Act"
    edns_host = nf_name
    mode = Mode.up
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    blocked_nflist = blocked_nf.split(",")
    batch = True
    stub = False

    tool_dict["nf_edns_host"][edns_host] = ["a2-er-s01-smfent-001", "b1-er-s02-smfent-001"]

    expected_success_list = ["a2-er-s01-smfent-001"]
    expected_failed_list = ["b1-er-s02-smfent-001"]
    expected_blocked_list = []
    tool_expected_value = "NG"

    nf_type = "smfent"
    module_name = "src.eri_smf_registration_process"
    class_name = "EriSmfRegistrationProcess"
    module_info = (nf_type, module_name, class_name)

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "Start Time: {}\n".format(logtime_str),
        "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]\n".format(tool_expected_value, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):SUCCESS={0}, FAILED={1}, BLOCKED={2}\n".format(len(expected_success_list), len(expected_failed_list), len(expected_blocked_list), mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of FAILED NF={0}, FAILED NF {1}\n".format(len(expected_failed_list), expected_failed_list, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of BLOCKED NF={0}, BLOCKED NF {1}\n".format(len(expected_blocked_list), expected_blocked_list, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "End Time: {}\n".format(logtime_str)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00111", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00115", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00116", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00117", expected_success_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00118", expected_failed_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00119", expected_blocked_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00120", tool_expected_value),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00112", None),
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_nf_module_info = mocker.Mock(return_value=module_info)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.import_module = mocker.Mock(return_value=None)
    test_mocker.getattr = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(side_effect=[ProcessStatus.post_check_ok, ProcessStatus.post_check_ng])
    mocker.patch("src.nf_registration_tool.import_module", test_mocker.import_module)
    mocker.patch("src.nf_registration_tool.getattr", test_mocker.getattr)
    mocker.patch("tests.test_nf_registration_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)
    mocker.patch("src.nf_registration_tool.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_nf_module_info", test_mocker.get_nf_module_info)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

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


def test_get_main11(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_main11 main試験11 準正常系試験 (UPモード, エイリアス, nf_name_list: 2NF, 1NF閉塞中失敗)

    試験条件
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "b1-CPA_East-Act"
    ・nf_name_list = ["a2-er-s01-smfent-001", "b1-er-s02-smfent-001"]
    ・mode = Mode.up
    ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfent-001"
    ・batch = True
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_modules"] = DICT_MODULES
    tool_dict["nf_infos"] = DICT_INFOS
    tool_dict["nf_edns_host"] = deepcopy(DICT_edns_host)

    nf_name = "b1-CPA_East-Act"
    edns_host = nf_name
    mode = Mode.up
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfent-001"
    blocked_nflist = blocked_nf.split(",")
    batch = True
    stub = False

    tool_dict["nf_edns_host"][edns_host] = ["a2-er-s01-smfent-001", "b1-er-s02-smfent-001"]

    expected_success_list = ["b1-er-s02-smfent-001"]
    expected_failed_list = []
    expected_blocked_list = ["a2-er-s01-smfent-001"]
    tool_expected_value = "OK"

    nf_type = "smfent"
    module_name = "src.eri_smf_registration_process"
    class_name = "EriSmfRegistrationProcess"
    module_info = (nf_type, module_name, class_name)

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "Start Time: {}\n".format(logtime_str),
        "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]\n".format(tool_expected_value, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):SUCCESS={0}, FAILED={1}, BLOCKED={2}\n".format(len(expected_success_list), len(expected_failed_list), len(expected_blocked_list), mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of FAILED NF={0}, FAILED NF {1}\n".format(len(expected_failed_list), expected_failed_list, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of BLOCKED NF={0}, BLOCKED NF {1}\n".format(len(expected_blocked_list), expected_blocked_list, mode=mode, time=logtime, edns_host=edns_host, nf_name=NF_NONE),
        "End Time: {}\n".format(logtime_str)
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00111", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00115", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00116", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00117", expected_success_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00118", expected_failed_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00119", expected_blocked_list),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00120", tool_expected_value),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00112", None),
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_host = edns_host
    test_mocker.nf_name = nf_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_nf_module_info = mocker.Mock(return_value=module_info)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.import_module = mocker.Mock(return_value=None)
    test_mocker.getattr = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(side_effect=[ProcessStatus.ssh_ng, ProcessStatus.post_check_ok])
    mocker.patch("src.nf_registration_tool.import_module", test_mocker.import_module)
    mocker.patch("src.nf_registration_tool.getattr", test_mocker.getattr)
    mocker.patch("tests.test_nf_registration_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)
    mocker.patch("src.nf_registration_tool.datetime", new=date_mock)

    tool = target.NfRegistrationTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_nf_module_info", test_mocker.get_nf_module_info)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

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
