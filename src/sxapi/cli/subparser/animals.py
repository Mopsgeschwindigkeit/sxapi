import json

from sxapi.cli import cli_user


def create_animals_parser(subparsers):
    animals_parser = subparsers.add_parser(
        "animals",
        help="Working on animals",
        usage="sxapi [base_options] animals [options]",
    )
    animals_parser.add_argument(
        "--ids",
        nargs="+",
        help="Ids of the animals to retrieve",
        metavar="ANIMAL_IDS",
    )
    animals_parser.add_argument(
        "--official-ids",
        nargs="+",
        help="Official ids of the animals to retrieve",
        metavar="OFFICIAL_IDS",
    )
    animals_parser.add_argument(
        "-o",
        "--organisation_id",
        nargs="?",
        default=None,
        help="Id of the organisation to retrieve animals from",
        metavar="ORGANISATION_ID",
    )
    animals_parser.add_argument(
        "--all",
        action="store_true",
        help="Retrieve all animals from the orga.(disables --ids,--official-ids)",
    )
    animals_parser.add_argument(
        "--limit",
        default=0,
        type=int,
        help="""
            Limit the number of animals to retrieve. (only active if --all is set).
        """,
        metavar="NUMBER OF ANIMALS",
    )
    animals_parser.add_argument(
        "--archived",
        action="store_true",
        default=False,
        help="Include archived animals. default = False. (only active if --all is set)",
    )

    animals_parser.set_defaults(func=animals_sub_function)


def animals_sub_function(args):
    if not cli_user.check_credentials_set():
        print("No credentials set!")
        return 1

    organisation_id = cli_user.organisation_id

    if args.organisation_id:
        organisation_id = args.organisation_id

    if organisation_id is None:
        print("No organisation_id set!")
        return 1

    animals = []

    if args.all:
        animals = cli_user.integration_v2_api.organisations.get_animals(
            organisation_id,
            include_archived=args.archived,
        )

        if args.limit > 0:
            animals = animals[: args.limit]

        print(json.dumps(animals))
        return 0

    if args.ids:
        animals = animals + cli_user.public_v2_api.animals.get_by_ids(args.ids)

    if args.official_ids:
        for official_id in args.official_ids:
            animals.append(
                cli_user.public_v2_api.animals.get_by_official_id(
                    organisation_id, official_id
                )
            )

    print(json.dumps(animals))
    return 0
