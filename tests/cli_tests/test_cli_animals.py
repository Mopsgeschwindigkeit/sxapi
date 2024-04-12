import json

import mock

from tests import (
    CliUserTest,
    ResponseMock,
    SxMainTestParser,
)

test_paser = SxMainTestParser(True)
args_parser = test_paser.parse_args
test_cli_user = CliUserTest()


@mock.patch("builtins.print")
@mock.patch("sxapi.cli.parser.main_parser.cli_user", test_cli_user)
@mock.patch("sxapi.cli.parser.subparser.animals.get.cli_user", test_cli_user)
def test_cli_animals_get(print_mock):
    # test output for all animals and organisation_id
    test_cli_user.integration_v2_api.mock_get_return_value(
        ResponseMock([{"all": "animals"}], 200)
    )

    # check for correct argument parsing
    namespace = args_parser(["animals", "get", "--organisation_id", "parent_orga_id"])
    assert namespace.animals_sub_commands == "get"
    assert namespace.ids is None
    assert namespace.official_ids is False
    assert namespace.organisation_id == "parent_orga_id"
    assert namespace.limit == 0
    assert namespace.archived is False

    # check if output was correctly printed to stdout
    assert print_mock.call_args[0][0] == '[{"all": "animals"}]'
    assert test_cli_user.integration_v2_api.get_called_with[0] == {
        "kwargs": {"json": {"include_archived": False}},
        "path": "/organisations/parent_orga_id/animals",
    }

    test_cli_user.integration_v2_api.reset_mock()

    # test output for multiple animals with id
    test_cli_user.public_v2_api.mock_get_return_value(
        ResponseMock(
            [
                {"animal_id": "1", "archived": True},
                {"animal_id": "2", "archived": False},
                {"animal_id": "3", "archived": True},
                {"animal_id": "4", "archived": True},
            ],
            200,
        )
    )

    # check for correct argument parsing
    namespace = args_parser(
        ["animals", "get", "--ids", "1", "2", "3", "4", "--limit", "2", "--archived"]
    )
    assert namespace.animals_sub_commands == "get"
    assert namespace.ids == ["1", "2", "3", "4"]
    assert namespace.official_ids is False
    assert namespace.organisation_id is None
    assert namespace.limit == 2
    assert namespace.archived is True

    # check if output was correctly printed to stdout
    assert (
        print_mock.call_args[0][0]
        == '[{"animal_id": "1", "archived": true}, {"animal_id": "3", "archived": true}]'
    )
    assert test_cli_user.public_v2_api.get_called_with[0] == {
        "kwargs": {"json": {"animal_ids": ["1", "2", "3", "4"]}},
        "path": "/animals/by_ids",
    }
    test_cli_user.public_v2_api.reset_mock()

    # test output for multiple animals with official id and archived
    animals_list = [
        {"animal_id": "1", "archived": True},
        {"animal_id": "2", "archived": False},
        {"animal_id": "3", "archived": True},
        {"animal_id": "4", "archived": True},
    ]
    test_cli_user.public_v2_api.mock_get_return_value(
        ResponseMock(animals_list, 200, iterator=True)
    )

    # check for correct argument parsing
    namespace = args_parser(
        ["animals", "get", "--ids", "1", "2", "3", "4", "--official-ids"]
    )
    assert namespace.animals_sub_commands == "get"
    assert namespace.ids == ["1", "2", "3", "4"]
    assert namespace.official_ids is True
    assert namespace.organisation_id is None
    assert namespace.limit == 0
    assert namespace.archived is False

    assert len(test_cli_user.public_v2_api.get_called_with) == 4
    for idx, a in enumerate(animals_list):
        assert test_cli_user.public_v2_api.get_called_with[idx] == {
            "kwargs": {"json": {}},
            "path": f"/animals/by_official_id/{test_cli_user.organisation_id}/{a['animal_id']}",
        }

    # check if output was correctly printed to stdout
    assert print_mock.call_args[0][0] == '[{"animal_id": "2", "archived": false}]'
    test_cli_user.public_v2_api.reset_mock()


@mock.patch("builtins.print")
@mock.patch("sxapi.cli.parser.main_parser.cli_user", test_cli_user)
@mock.patch("sxapi.cli.parser.subparser.animals.create.cli_user", test_cli_user)
def test_cli_animals_create(print_mock):
    test_cli_user.public_v2_api.mock_post_return_value(
        ResponseMock(
            {
                "_id": "1",
                "archived": True,
                "mark": "test_mark",
                "name": "test_name",
                "lifecycle": {},
            },
            200,
        )
    )

    namespace = args_parser(
        ["animals", "create", "./tests/cli_tests/animal_test_json.json"]
    )
    assert namespace.animals_sub_commands == "create"
    assert namespace.organisation_id is None
    assert namespace.animal_json.name == "./tests/cli_tests/animal_test_json.json"

    assert len(test_cli_user.public_v2_api.post_called_with) == 1

    # if the organisation_id is set in the json file, it should be ignored
    comp_dict = json.load(open("./tests/cli_tests/animal_test_json.json"))
    comp_dict["organisation_id"] = test_cli_user.organisation_id
    assert test_cli_user.public_v2_api.post_called_with[0] == {
        "kwargs": {"json": comp_dict},
        "path": "/animals",
    }

    assert (
        print_mock.call_args_list[0][0][0]
        == "Ignoring organisation_id from json file, use from organisation_id from config."
    )

    comp_dict = {
        "_id": "1",
        "archived": True,
        "mark": "test_mark",
        "name": "test_name",
        "lifecycle": {},
    }
    assert print_mock.call_args_list[1][0][0] == comp_dict


@mock.patch("builtins.print")
@mock.patch("sxapi.cli.parser.main_parser.cli_user", test_cli_user)
@mock.patch("sxapi.cli.parser.subparser.animals.update.cli_user", test_cli_user)
def test_cli_animals_update(print_mock):
    test_cli_user.public_v2_api.mock_put_return_value(
        ResponseMock(
            {
                "_id": "1",
                "archived": True,
                "mark": "test_mark",
                "name": "test_name",
                "lifecycle": {},
            },
            200,
        )
    )

    namespace = args_parser(
        ["animals", "update", "./tests/cli_tests/animal_test_json.json"]
    )
    assert namespace.animals_sub_commands == "update"
    assert namespace.organisation_id is None
    assert namespace.update_dict.name == "./tests/cli_tests/animal_test_json.json"

    assert len(test_cli_user.public_v2_api.put_called_with) == 1

    # if the organisation_id is set in the json file, it should be ignored
    comp_dict = json.load(open("./tests/cli_tests/animal_test_json.json"))
    comp_dict["organisation_id"] = test_cli_user.organisation_id
    a = comp_dict.pop("animal_id")
    assert test_cli_user.public_v2_api.put_called_with[0] == {
        "kwargs": {"json": comp_dict},
        "path": f"/animals/{a}",
    }

    assert (
        print_mock.call_args_list[0][0][0]
        == "Ignoring organisation_id from json file, use from organisation_id from config."
    )

    comp_dict = {
        "_id": "1",
        "archived": True,
        "mark": "test_mark",
        "name": "test_name",
        "lifecycle": {},
    }
    assert print_mock.call_args_list[1][0][0] == comp_dict
