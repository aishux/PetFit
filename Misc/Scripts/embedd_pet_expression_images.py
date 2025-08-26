import numpy as np

from pytidb import TiDBClient
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction
import os
from dotenv import load_dotenv
from PIL import Image
import time


load_dotenv()


# ── CONFIG ────────────────────────────────────────────────────────────────
TIDB_HOST = os.getenv("TIDB_HOST")
TIDB_USER = os.getenv("TIDB_USER")
TIDB_PASS = os.getenv("TIDB_PASS")
TIDB_PORT = os.getenv("TIDB_PORT")
TIDB_DATABASE = os.getenv("TIDB_DATABASE")
JINA_AI_API_KEY = os.getenv("JINA_AI_API_KEY")
# ── END CONFIG ────────────────────────────────────────────────────────────


TIDB_DATABASE_URL=f"mysql+pymysql://{TIDB_USER}:{TIDB_PASS}@{TIDB_HOST}:{TIDB_PORT}/{TIDB_DATABASE}?ssl_ca=/etc/ssl/cert.pem"

db = TiDBClient.connect(TIDB_DATABASE_URL)


image_embed = EmbeddingFunction(
    model_name="jina_ai/jina-embeddings-v4",
    api_key=JINA_AI_API_KEY,
    multimodal=True,
    timeout=90
)

angry_image_urls = ["https://iili.io/K2f1CZu.jpg","https://iili.io/K2f1oCb.jpg","https://iili.io/K2f1xGj.jpg","https://iili.io/K2f1z6x.jpg","https://iili.io/K2f1T3Q.jpg","https://iili.io/K2f1uaV.jpg","https://iili.io/K2f1RyP.jpg","https://iili.io/K2f1A8B.jpg","https://iili.io/K2f17u1.jpg","https://iili.io/K2f1YwF.jpg","https://iili.io/K2f1aZg.jpg","https://iili.io/K2f1lna.jpg","https://iili.io/K2f10MJ.jpg","https://iili.io/K2f116v.jpg","https://iili.io/K2f1Map.jpg","https://iili.io/K2f1V8N.jpg","https://iili.io/K2f1X9I.jpg","https://iili.io/K2f1hut.jpg","https://iili.io/K2f1jwX.jpg","https://iili.io/K2f1wtn.jpg","https://iili.io/K2f1Ons.jpg","https://iili.io/K2f1eMG.jpg","https://iili.io/K2f1Scl.jpg","https://iili.io/K2f18F4.jpg","https://iili.io/K2f1US2.jpg","https://iili.io/K2f1r9S.jpg","https://iili.io/K2f16N9.jpg","https://iili.io/K2f1Pte.jpg","https://iili.io/K2f1sou.jpg","https://iili.io/K2f1LMb.jpg","https://iili.io/K2f1QPj.jpg","https://iili.io/K2f1tKx.jpg","https://iili.io/K2f1DcQ.jpg","https://iili.io/K2f1bSV.jpg","https://iili.io/K2f1pHB.jpg","https://iili.io/K2f1yAP.jpg","https://iili.io/K2fE9N1.jpg","https://iili.io/K2fEHDF.jpg","https://iili.io/K2fEdog.jpg","https://iili.io/K2fE2Va.jpg","https://iili.io/K2fE3iJ.jpg","https://iili.io/K2fEKKv.jpg","https://iili.io/K2fEflR.jpg","https://iili.io/K2fEqSp.jpg","https://iili.io/K2fECHN.jpg","https://iili.io/K2fEnRI.jpg","https://iili.io/K2fEoNt.jpg","https://iili.io/K2fExDX.jpg","https://iili.io/K2fEIxn.jpg","https://iili.io/K2fETVs.jpg","https://iili.io/K2fEuiG.jpg","https://iili.io/K2fERff.jpg","https://iili.io/K2fE5l4.jpg","https://iili.io/K2fE7Ul.jpg","https://iili.io/K2fEaJ2.jpg","https://iili.io/K2fEcRS.jpg","https://iili.io/K2fElO7.jpg","https://iili.io/K2fE0b9.jpg","https://iili.io/K2fEExe.jpg","https://iili.io/K2fEGWu.jpg","https://iili.io/K2fEMib.jpg","https://iili.io/K2fEWfj.jpg","https://iili.io/K2fEhUQ.jpg","https://iili.io/K2fEX0x.jpg","https://iili.io/K2fEwJV.jpg","https://iili.io/K2fEN5B.jpg","https://iili.io/K2fEeb1.jpg","https://iili.io/K2fEOOP.jpg","https://iili.io/K2fEvzF.jpg","https://iili.io/K2fE8Wg.jpg","https://iili.io/K2fESsa.jpg","https://iili.io/K2fEgqJ.jpg","https://iili.io/K2fEr0v.jpg","https://iili.io/K2fE4gR.jpg","https://iili.io/K2fEi5N.jpg"]

sad_image_urls = ["https://iili.io/K2q21l2.jpg","https://iili.io/K2q2MH7.jpg","https://iili.io/K2q20Kl.jpg","https://iili.io/K2q2ESS.jpg","https://iili.io/K2q2WNe.jpg","https://iili.io/K2q2job.jpg","https://iili.io/K2q2XDu.jpg","https://iili.io/K2q2Nix.jpg","https://iili.io/K2q2eKQ.jpg","https://iili.io/K2q2klV.jpg","https://iili.io/K2q2vUB.jpg","https://iili.io/K2q2SHP.jpg","https://iili.io/K2q2gOF.jpg","https://iili.io/K2q2UR1.jpg","https://iili.io/K2q2rDg.jpg","https://iili.io/K2q26xa.jpg","https://iili.io/K2q2PWJ.jpg","https://iili.io/K2q2iiv.jpg","https://iili.io/K2q2LfR.jpg","https://iili.io/K2q2Qlp.jpg","https://iili.io/K2q2DJI.jpg","https://iili.io/K2q2mOX.jpg","https://iili.io/K2q2pbn.jpg","https://iili.io/K2q39xs.jpg","https://iili.io/K2q3HWG.jpg","https://iili.io/K2q32f4.jpg","https://iili.io/K2q330l.jpg","https://iili.io/K2q3Fg2.jpg","https://iili.io/K2q3Cbe.jpg","https://iili.io/K2q3ozu.jpg","https://iili.io/K2q3xWb.jpg","https://iili.io/K2q3zsj.jpg","https://iili.io/K2q3Tqx.jpg","https://iili.io/K2q3u0Q.jpg","https://iili.io/K2q3AgV.jpg","https://iili.io/K2q35dB.jpg","https://iili.io/K2q375P.jpg","https://iili.io/K2q3Ye1.jpg","https://iili.io/K2q3amF.jpg","https://iili.io/K2q30Xa.jpg","https://iili.io/K2q3Gqv.jpg","https://iili.io/K2q3M1R.jpg","https://iili.io/K2q3Vgp.jpg","https://iili.io/K2q3h7I.jpg","https://iili.io/K2q3wmX.jpg","https://iili.io/K2q3OIn.jpg","https://iili.io/K2q3eXs.jpg","https://iili.io/K2q38Bf.jpg","https://iili.io/K2q3r22.jpg","https://iili.io/K2q347S.jpg","https://iili.io/K2q36k7.jpg","https://iili.io/K2q3sIe.jpg","https://iili.io/K2q3QLb.jpg","https://iili.io/K2q3tBj.jpg","https://iili.io/K2q3DEx.jpg","https://iili.io/K2q3p2V.jpg","https://iili.io/K2qF9kP.jpg","https://iili.io/K2qFdTF.jpg","https://iili.io/K2qF2hg.jpg","https://iili.io/K2qF3Qa.jpg","https://iili.io/K2qFfEv.jpg","https://iili.io/K2qFq4R.jpg","https://iili.io/K2qFC2p.jpg","https://iili.io/K2qFnYN.jpg","https://iili.io/K2qFovI.jpg","https://iili.io/K2qFxpt.jpg","https://iili.io/K2qFITX.jpg","https://iili.io/K2qFTjn.jpg","https://iili.io/K2qFRCG.jpg","https://iili.io/K2qF5Gf.jpg","https://iili.io/K2qF744.jpg","https://iili.io/K2qFa3l.jpg","https://iili.io/K2qFlvS.jpg","https://iili.io/K2qF0y7.jpg","https://iili.io/K2qFEu9.jpg","https://iili.io/K2qFGje.jpg","https://iili.io/K2qFMZu.jpg","https://iili.io/K2qFWCb.jpg","https://iili.io/K2qFXGj.jpg","https://iili.io/K2qFh6x.jpg","https://iili.io/K2qFNaV.jpg","https://iili.io/K2qFO8B.jpg","https://iili.io/K2qFeyP.jpg","https://iili.io/K2qFvu1.jpg"]

happy_image_urls = ["https://iili.io/K2fiZSR.jpg","https://iili.io/K2fiLKJ.jpg","https://iili.io/K2fiiPa.jpg","https://iili.io/K2fiQcv.jpg","https://iili.io/K2fiD9p.jpg","https://iili.io/K2fibAN.jpg","https://iili.io/K2fs9oX.jpg","https://iili.io/K2fsHVn.jpg","https://iili.io/K2fsJPs.jpg","https://iili.io/K2fs2KG.jpg","https://iili.io/K2fs3lf.jpg","https://iili.io/K2fsFS4.jpg","https://iili.io/K2fsqR2.jpg","https://iili.io/K2fsBNS.jpg","https://iili.io/K2fsziu.jpg","https://iili.io/K2fsTKb.jpg","https://iili.io/K2fsAUx.jpg","https://iili.io/K2fs5HQ.jpg","https://iili.io/K2fsaDP.jpg","https://iili.io/K2fsYOB.jpg","https://iili.io/K2fslx1.jpg","https://iili.io/K2fs0WF.jpg","https://iili.io/K2fs1ig.jpg","https://iili.io/K2fsGfa.jpg","https://iili.io/K2fsM0J.jpg","https://iili.io/K2fsXJR.jpg","https://iili.io/K2fshRp.jpg","https://iili.io/K2fsjON.jpg","https://iili.io/K2fswbI.jpg","https://iili.io/K2fsOxt.jpg","https://iili.io/K2fseWX.jpg","https://iili.io/K2fsksn.jpg","https://iili.io/K2fs8fs.jpg","https://iili.io/K2fs6e2.jpg","https://iili.io/K2fsUgf.jpg","https://iili.io/K2fsrJ4.jpg","https://iili.io/K2fs45l.jpg","https://iili.io/K2fssz7.jpg","https://iili.io/K2fsQse.jpg","https://iili.io/K2fsLX9.jpg","https://iili.io/K2fstqu.jpg","https://iili.io/K2fspdx.jpg","https://iili.io/K2fL9eV.jpg","https://iili.io/K2fsy5Q.jpg","https://iili.io/K2fLHmB.jpg","https://iili.io/K2fL2X1.jpg","https://iili.io/K2fLKqg.jpg","https://iili.io/K2fL3LF.jpg","https://iili.io/K2fLf1a.jpg","https://iili.io/K2fLn7R.jpg","https://iili.io/K2fLoep.jpg","https://iili.io/K2fLCdv.jpg","https://iili.io/K2fLxmN.jpg","https://iili.io/K2fLIII.jpg","https://iili.io/K2fLTXt.jpg","https://iili.io/K2fLuLX.jpg","https://iili.io/K2fLRBn.jpg","https://iili.io/K2fL51s.jpg","https://iili.io/K2fL7rG.jpg","https://iili.io/K2fLa2f.jpg","https://iili.io/K2fLc74.jpg","https://iili.io/K2fLlkl.jpg","https://iili.io/K2fL0p2.jpg","https://iili.io/K2fLEIS.jpg","https://iili.io/K2fLGh7.jpg","https://iili.io/K2fLMQ9.jpg","https://iili.io/K2fLWBe.jpg","https://iili.io/K2fLXEu.jpg","https://iili.io/K2fLhrb.jpg","https://iili.io/K2fL8hP.jpg","https://iili.io/K2fLSQ1.jpg","https://iili.io/K2fLgCF.jpg","https://iili.io/K2fL44a.jpg","https://iili.io/K2fLP3J.jpg","https://iili.io/K2fLiYv.jpg","https://iili.io/K2fLsvR.jpg","https://iili.io/K2fLLpp.jpg","https://iili.io/K2fLtjI.jpg","https://iili.io/K2fLDQt.jpg","https://iili.io/K2fLmCX.jpg","https://iili.io/K2fLy4s.jpg","https://iili.io/K2fQH3G.jpg","https://iili.io/K2fQdv4.jpg","https://iili.io/K2fQJaf.jpg","https://iili.io/K2fQ2yl.jpg","https://iili.io/K2fQFu2.jpg","https://iili.io/K2fQKjS.jpg","https://iili.io/K2fQfZ7.jpg","https://iili.io/K2fQCGe.jpg","https://iili.io/K2fQzaj.jpg"]

class PetExpressionsIdentification(TableModel, table=True):
    __tablename__ = "pet_expression_identification"

    id: int = Field(primary_key=True)
    expression_identification: str = Field()
    image_uri: str = Field()
    image_vec: list[float] = image_embed.VectorField(
        source_field="image_uri"
    )

# table = db.create_table(schema=PetExpressionsIdentification, if_exists='skip')

# print("Connected to TiDB database and created table!")

# items_lst = []
# count = 0
# for exp in {"angry":angry_image_urls, "sad": sad_image_urls, "happy": happy_image_urls}.items():
#     for img_url in exp[1]:
#         items_lst.append(PetExpressionsIdentification(
#             id = 11231412 + count,
#             expression_identification=exp[0],
#             image_uri = img_url
#         ))
#         count += 1

#     table.bulk_insert(items_lst)
#     print(f"Inserted data for expression: {exp[0]}")
#     items_lst = []

#     time.sleep(60)


# print("Inserted all the data into the table!")

table = db.open_table("pet_expression_identification")

# image = Image.open("../Datasets/PetExpressions/test/Angry/14.jpg")

# results = table.search("https://iili.io/K2nt9hx.jpg").limit(1).to_list()
results = table.search("https://iili.io/K2nDkRn.jpg").limit(1).to_list()

print(results)