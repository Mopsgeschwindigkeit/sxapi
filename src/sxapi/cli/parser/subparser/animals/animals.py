import json

from sxapi.cli import cli_user


class SxApiAnimalsSubparser:
    @classmethod
    def register_as_subparser(cls, parent_subparser):
        return cls(parent_subparser)

    def __init__(self, parent_subparser, subparsers=False):
        self._parser = parent_subparser.add_parser(
            "animals",
            help="Working on animals",
            usage="sxapi [base_options] animals [options]",
        )

        self._add_arguments()
        self._set_default_func()

        if subparsers:
            self.reg_subparsers = []
            self._subparsers = self._parser.add_subparsers(
                title="Sub Commands",
                description="Available subcommands:",
                dest="animals_sub_commands",
            )

            self._add_subparser()

    def _add_arguments(self):
        self._parser.add_argument(
            "--ids",
            nargs="+",
            help="Ids of the animals to retrieve",
            metavar="ANIMAL_IDS",
        )
        self._parser.add_argument(
            "-d",
            "--delete",
            action="store_true",
            help="Delete animals",
        )
        self._parser.add_argument(
            "--official-ids",
            nargs="+",
            help="Official ids of the animals to retrieve",
            metavar="OFFICIAL_IDS",
        )
        self._parser.add_argument(
            "-o",
            "--organisation_id",
            nargs="?",
            default=None,
            help="Id of the organisation to retrieve animals from",
            metavar="ORGANISATION_ID",
        )
        self._parser.add_argument(
            "--all",
            action="store_true",
            help="Retrieve all animals from the orga.(disables --ids,--official-ids)",
        )
        self._parser.add_argument(
            "--limit",
            default=0,
            type=int,
            help="""
                    Limit the number of animals to retrieve.
                """,
            metavar="NUMBER OF ANIMALS",
        )
        self._parser.add_argument(
            "--archived",
            action="store_true",
            default=False,
            help="Include archived animals. \
                  default = False. (only active if --all is set)",
        )

    def _add_subparser(self):
        pass

    def _set_default_func(self):
        def animals_sub_function(args):
            if not cli_user.check_credentials_set():
                print("No credentials set!")
                return 1

            # check for arguments and print help text
            if not args.ids and not args.official_ids and not args.all:
                self._parser.print_help()
                return 2

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

            if args.ids:
                animals = animals + cli_user.public_v2_api.animals.get_by_ids(args.ids)

            if args.official_ids:
                for official_id in args.official_ids:
                    animals.append(
                        cli_user.public_v2_api.animals.get_by_official_id(
                            organisation_id, official_id
                        )
                    )

            if args.limit > 0:
                animals = animals[: args.limit]

            print(json.dumps(animals))
            return 0

        self._parser.set_defaults(func=animals_sub_function)
