import json

import mock

from sxapi.cli.cli import Cli
from sxapi.cli.cli_user import CliUser
from sxapi.cli.subparser.animals import animals_sub_function

args_parser = Cli.parse_args

TestApiV2 = mock.MagicMock()
TestIntegrationV2 = mock.MagicMock()

test_config_dict = {
    "user": "TestUser",
    "pwd": "TestPassword",
    "orga": "TestOrgaId",
    "api_public_v2_path": TestApiV2,
    "api_integration_v2_path": TestIntegrationV2,
}

test_cli_user = CliUser()
test_cli_user.init_user(test_config_dict, "test_cli_user_token", False)

animal_list = [{"name": "animal1"}, {"name": "animal2"}, {"name": "animal3"}]
animal_oid = {"name": "animal_o_id"}


@mock.patch("builtins.print")
@mock.patch("sxapi.cli.subparser.animals.cli_user", test_cli_user)
@mock.patch("sxapi.publicV2.animals.Animals.get_by_ids", return_value=animal_list)
@mock.patch(
    "sxapi.publicV2.animals.Animals.get_by_official_id", return_value=animal_oid
)
def test_animals_ids_and_oids(gboi_mock, gbi_mock, print_mock):
    namespace = args_parser(
        ["animals", "--ids", "1", "2", "3", "--official-ids", "o4", "o5", "o6"]
    )
    assert namespace.ids == ["1", "2", "3"]
    assert namespace.official_ids == ["o4", "o5", "o6"]
    assert namespace.organisation_id is None
    assert namespace.all is False
    assert namespace.limit == 0
    assert namespace.archived is False
    assert namespace.func == animals_sub_function

    animals_sub_function(namespace)
    gbi_mock.assert_called_once_with(["1", "2", "3"])

    calls = [
        mock.call("TestOrgaId", "o4"),
        mock.call("TestOrgaId", "o5"),
        mock.call("TestOrgaId", "o6"),
    ]

    gboi_mock.assert_has_calls(calls)
    print_mock.assert_called_once_with(json.dumps(animal_list + 3 * [animal_oid]))


@mock.patch("builtins.print")
@mock.patch("sxapi.cli.subparser.animals.cli_user", test_cli_user)
@mock.patch("sxapi.publicV2.animals.Animals.get_by_ids")
@mock.patch("sxapi.publicV2.animals.Animals.get_by_official_id")
@mock.patch(
    "sxapi.integrationV2.organisations.Organisations.get_animals",
    return_value=animal_list,
)
def test_all(all_mock, gboi_mock, gbi_mock, print_mock):
    namespace = args_parser(
        ["animals", "-o", "orga_id", "--all", "--ids", "1", "2", "--official-ids", "3"]
    )
    assert namespace.ids == ["1", "2"]
    assert namespace.official_ids == ["3"]
    assert namespace.organisation_id == "orga_id"
    assert namespace.all is True
    assert namespace.limit == 0
    assert namespace.archived is False
    assert namespace.func == animals_sub_function

    animals_sub_function(namespace)
    gbi_mock.assert_not_called()
    gboi_mock.assert_not_called()
    all_mock.assert_called_once_with("orga_id", include_archived=False)
    print_mock.assert_called_once_with(json.dumps(animal_list))


@mock.patch("builtins.print")
@mock.patch("sxapi.cli.subparser.animals.cli_user", test_cli_user)
@mock.patch("sxapi.publicV2.animals.Animals.get_by_ids")
@mock.patch("sxapi.publicV2.animals.Animals.get_by_official_id")
@mock.patch(
    "sxapi.integrationV2.organisations.Organisations.get_animals",
    return_value=animal_list,
)
def test_all_limit(all_mock, gboi_mock, gbi_mock, print_mock):
    namespace = args_parser(
        ["animals", "--all", "--ids", "1", "2", "--official-ids", "3", "--limit", "1"]
    )
    assert namespace.ids == ["1", "2"]
    assert namespace.official_ids == ["3"]
    assert namespace.organisation_id is None
    assert namespace.all is True
    assert namespace.limit == 1
    assert namespace.archived is False
    assert namespace.func == animals_sub_function

    animals_sub_function(namespace)
    gbi_mock.assert_not_called()
    gboi_mock.assert_not_called()
    all_mock.assert_called_once_with("TestOrgaId", include_archived=False)
    print_mock.assert_called_once_with(json.dumps(animal_list[:1]))
