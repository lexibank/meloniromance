import pathlib
import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Language
from pylexibank import FormSpec


@attr.s
class CustomLanguage(Language):
    NameInSource = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "meloniromance"
    language_class = CustomLanguage
    form_spec = FormSpec(separators="~;,/", missing_data=["∅"], first_form_only=True)

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        languages = args.writer.add_languages(lookup_factory="NameInSource")

        # read in data
        data = self.raw_dir.read_csv(
            "data.tsv", delimiter="\t", dicts=True
        )
        # add data
        for i, row in pb(enumerate(data), desc="cldfify", total=len(data)):
            cog = str(i+1)
            cid = "concept_"+cog
            args.writer.add_concept(
                    ID=cid,
                    Name=cid,
                    )
            for language, lid in languages.items():
                entry = row[language]
                if not entry.strip() == '-':
                    lex = args.writer.add_form(
                            Language_ID=lid,
                            Parameter_ID=cid,
                            Value=entry,
                            Form=entry,
                            Cognacy=cog,
                            Source="Meloni2021"
                            )
                    args.writer.add_cognate(
                            lexeme=lex,
                            Cognateset_ID=cog
                            )



