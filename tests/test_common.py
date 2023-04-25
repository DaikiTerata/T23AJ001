from datetime import datetime
import io
import json
import pathlib
from typing import Any, List
from unittest.mock import MagicMock
import pytest
from pytest_mock import MockerFixture

import src.nf_registration_common as common
from xgnlog.Log import Level


JOB_ID = "T22AJ000"


def get_1st_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("1st_nf_reg_common.log")


def get_2nd_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("2nd_nf_reg_common.log")


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


def test_MESSAGES01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_MESSAGES01 MESSAGES試験01 正常試験

    試験条件
    ・nf_registration_common module import時に実行

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    ・結果が想定したdictであること
    """
    expected_value = {
        "M0000": "[RESULT]:{mode}:{time}:{edns_host}({nf_name}):[ {0} ]",
        "M0001": "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):SUCCESS={0}, FAILED={1}, BLOCKED={2}",
        "M0002": "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of FAILED NF={0}, FAILED NF {1}",
        "M0003": "[DETAIL]:{mode}:{time}:{edns_host}({nf_name}):# of BLOCKED NF={0}, BLOCKED NF {1}",
        "M0010": "[INFO]:{mode}:{time}:{edns_host}({nf_name}):nf registration current status is {0}. [ {1} ]",
        "M0011": "[SUCCESS]:{mode}:{time}:{edns_host}({nf_name}):nf registration current status is already {0}. [ {1} ]",
        "M0012": "[SUCCESS]:{mode}:{time}:{edns_host}({nf_name}):nf registration current status is {0}. [ {1} ]",
        "M0099": "[INFO]:{mode}:{time}:{edns_host}({nf_name}):script was aborted due to an interractive action.",
        "M9000": "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):failed to analyse arguments {0}.",
        "M9001": "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):configuration files not found. file={0}",
        "M9002": "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):failed to analyse configuration files. file={0}",
        "M9003": "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):required json key not found. file={0}, key={1}",
        "M9010": "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):nf configuration not found.",
        "M9011": "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):ssh bastion {0} setting something wrong. [ UNKNOWN ]",
        "M9020": "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):ssh connection timeout was happened. [ UNKNOWN ]",
        "M9021": "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):ssh process coundn't connect to nf or bastion. [ UNKNOWN ]",
        "M9030": "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):nf registration currentry status couldn't get or mismatch. [ UNKNOWN ]",
        "M9040": "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):nf registration status couldn't change... still {0}. [ {1} ]",
        "M9041": "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):status change was failed. abort has done. current status is {0}. [ {1} ]",
        "M9042": "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):commit was failed. abort has done."
    }

    assert common.MESSAGES is not None
    assert isinstance(common.MESSAGES, dict)
    assert common.MESSAGES == expected_value


def test_json_check_and_load01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_json_check_and_load01 json_check_and_load試験01 正常試験

    試験条件
    ・対象ファイル: config/nf-registration-tool.json
    ・必須キー: ("nf_modules", "nf_infos", "nf_edns_host")

    試験結果
    ・Exceptionが発生しないこと
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    ・関数結果が想定したdictであること
    """
    filepath = pathlib.Path("config/nf-registration-tool.json")
    req_key = ("nf_modules", "nf_infos", "nf_edns_host")
    expected_value = {
        "nf_modules": "nf-modules.json",
        "nf_infos": "nf-infos.json",
        "nf_edns_host": "nf-edns_host.json"
    }

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00001", filepath),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00002", None)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_common.LOGGER", new=logger)

    response_value = common.json_check_and_load(filepath, req_key)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value is not None
    assert isinstance(response_value, dict)
    assert response_value == expected_value
    assert log_path_1st.exists()
    assert len(response_value_log_1st) == len(expected_log_1st)
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_json_check_and_load02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_json_check_and_load02 json_check_and_load試験02 異常試験 (ファイルなし)

    試験条件
    ・対象ファイル: tests/config/not_exist_file.json (ファイルなし)
    ・必須キー: ("nf_modules", "nf_infos", "nf_edns_host")

    試験結果
    ・FileNotFoundErrorが発生すること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    filepath = pathlib.Path("tests/config/not_exist_file.json")
    req_key = ("nf_modules", "nf_infos", "nf_edns_host")
    expected_value = None

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00001", filepath)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_common.LOGGER", new=logger)

    with pytest.raises(FileNotFoundError) as exc_info:
        response_value = common.json_check_and_load(filepath, req_key)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert exc_info.type is FileNotFoundError
    assert exc_info.value.filename == str(filepath)
    assert log_path_1st.exists()
    assert len(response_value_log_1st) == len(expected_log_1st)
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_json_check_and_load03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_json_check_and_load03 json_check_and_load試験03 異常試験 (jsonデコードエラー)

    試験条件
    ・対象ファイル: tests/config/not_json.txt (JSON形式以外)
    ・必須キー: ("nf_modules", "nf_infos", "nf_edns_host")

    試験結果
    ・json.JSONDecodeErrorが発生すること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    filepath = pathlib.Path("tests/config/not_json.txt")
    req_key = ("nf_modules", "nf_infos", "nf_edns_host")
    expected_value = None

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00001", filepath)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_common.LOGGER", new=logger)

    with pytest.raises(json.JSONDecodeError) as exc_info:
        response_value = common.json_check_and_load(filepath, req_key)

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert exc_info.type is json.JSONDecodeError
    assert log_path_1st.exists()
    assert len(response_value_log_1st) == len(expected_log_1st)
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_out_message01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture, monkeypatch):
    """test_out_message01 out_message試験01 正常試験 (メッセージテンプレート)

    試験条件
    ・msg_key = M0010
    ・mode = common.Mode.down
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・fills = ("deregistered", "DOWN")

    試験結果
    ・Exceptionが発生しないこと
    ・テンプレート"[INFO]:{mode}:{time}:{edns_host}({nf_name}):nf registration current status is {0}. [ {1} ]",にデータが埋め込まれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    msg_key = "M0010"
    mode = common.Mode.down
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    logtime = "1994-12-03 12:34:56"
    fills = ("deregistered", "DOWN")
    template = "[INFO]:{mode}:{time}:{edns_host}({nf_name}):nf registration current status is {0}. [ {1} ]"
    expected_value = template.format(mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name, *fills)

    expected_sout = [
        expected_value + "\n"
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00003", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00004", expected_value)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_common.LOGGER", new=logger)

    date_mock = MagicMock()
    date_mock.now = mocker.Mock(return_value=datetime(1994, 12, 3, 12, 34, 56))
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    response_value = common.out_message(msg_key, mode, edns_host, nf_name, *fills)

    # stdout, stderr確認
    (sout, serr) = capsys.readouterr()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value is None
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_out_message02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture, monkeypatch):
    """test_out_message02 out_message試験02 正常試験 (テンプレート、fillsなし)

    試験条件
    ・msg_key = "M9021"
    ・mode = common.Mode.up
    ・edns_host = "b1-CPA_East-Act"
    ・nf_name = "a2-er-s01-smfent-001"
    ・fills: なし

    試験結果
    ・Exceptionが発生しないこと
    ・テンプレート"[ERROR]:{mode}:{time}:{node}({target_nf}):ssh process coundn't connect smfvoice or bastion. [ UNKNOWN ]"にデータが埋め込まれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    msg_key = "M9021"
    mode = common.Mode.up
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    fills = None
    logtime = "1994-12-03 12:34:56"
    template = "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):ssh process coundn't connect to nf or bastion. [ UNKNOWN ]"
    expected_value = template.format(mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)

    expected_sout = [
        expected_value + "\n"
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00003", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00004", expected_value)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_common.LOGGER", new=logger)

    date_mock = MagicMock()
    date_mock.now = mocker.Mock(return_value=datetime(1994, 12, 3, 12, 34, 56))
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    response_value = common.out_message(msg_key, mode, edns_host, nf_name, fills)

    # stdout, stderr確認
    (sout, serr) = capsys.readouterr()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value is None
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_out_message03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture, monkeypatch):
    """test_out_message03 out_message試験03 正常試験 (自作テンプレート)

    試験条件
    ・対象メッセージID: M901
    ・mode: co
    ・node: NODE_NONE
    ・target: TARGET_NONE
    ・fills: ["NO_MODE", "NO_P-CSCF", "", "--batch"]

    試験結果
    ・Exceptionが発生しないこと
    ・自作テンプレート"[ERROR]:{mode}:{time}:{edns_host}({nf_name}):Failed to analyse arguments {0}."にデータが埋め込まれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    msg_key = "M9000"
    mode = common.Mode.show
    edns_host = "b1-CPA_East-Act"
    nf_name = "a2-er-s01-smfent-001"
    fills = [mode, edns_host, nf_name, "--batch"]
    logtime = "1994-12-03 12:34:56"

    fills = ["NO_MODE", "NO_P-CSCF", "", "--batch"]
    template = "[ERROR]:{mode}:{time}:{edns_host}({nf_name}):Failed to analyse arguments {0}."
    expected_value = template.format(fills, mode=mode, time=logtime, edns_host=edns_host, nf_name=nf_name)

    expected_sout = [
        expected_value + "\n"
    ]

    expected_log_1st = [
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00003", None),
        "job_id:{0}, message_id:{1}, add_info:{2}\n".format(JOB_ID, "I00004", expected_value)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.nf_registration_common.LOGGER", new=logger)

    date_mock = MagicMock()
    date_mock.now = mocker.Mock(return_value=datetime(1994, 12, 3, 12, 34, 56))
    mocker.patch("src.nf_registration_common.datetime", new=date_mock)

    response_value = common.out_message(msg_key, mode, edns_host, nf_name, fills, template=template)

    # stdout, stderr確認
    (sout, serr) = capsys.readouterr()

    # 結果確認
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value is None
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_interactive_check01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch):
    """test_interactive_check01 interactive_check試験01 正常系試験 (interractive: "y")

    試験条件
    ・入力指示で「y」
    ・大文字小文字区別なし

    試験結果
    ・Exceptionが発生しないこと
    ・結果が(True, "y")となること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    message = "Please input [Y] for next action, or [N] for abort.: "
    continue_list = ["y", "ye", "yes"]
    abort_list = ["n", "no"]
    interact_input = "y"

    expected_value = (True, interact_input)

    expected_sout = [
        message
    ]

    expected_log_1st = []

    expected_log_2nd = []

    monkeypatch.setattr("sys.stdin", io.StringIO(interact_input + "\n"))
    response_value = common.interactive_check(message, continue_list, abort_list)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_interactive_check02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch):
    """test_interactive_check02 interactive_check試験02 正常系試験 (interractive: "n")

    試験条件
    ・入力指示で「n」
    ・大文字小文字区別なし

    試験結果
    ・Exceptionが発生しないこと
    ・結果が(False, "n")となること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    message = "Please input [Y] for next action, or [N] for abort.: "
    continue_list = ["y", "ye", "yes"]
    abort_list = ["n", "no"]
    interact_input = "n"

    expected_value = (False, interact_input)

    expected_sout = [
        message
    ]

    expected_log_1st = []

    expected_log_2nd = []

    monkeypatch.setattr("sys.stdin", io.StringIO(interact_input + "\n"))
    response_value = common.interactive_check(message, continue_list, abort_list)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_interactive_check03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch):
    """test_interactive_check03 interactive_check試験03 正常系試験 (interractive: "Y, y")

    試験条件
    ・入力指示で「Y」、「y」
    ・大文字小文字区別あり

    試験結果
    ・Exceptionが発生しないこと
    ・結果が(True, "y")となること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    message = "Please input [Y] for next action, or [N] for abort.: "
    continue_list = ["y", "ye", "yes"]
    abort_list = ["n", "no"]
    interact_input = ["Y", "y"]

    expected_value = (True, interact_input[1])

    expected_sout = [
        message + message
    ]

    expected_log_1st = []

    expected_log_2nd = []

    monkeypatch.setattr("sys.stdin", io.StringIO("\n".join(interact_input) + "\n"))
    response_value = common.interactive_check(message, continue_list, abort_list, True)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
