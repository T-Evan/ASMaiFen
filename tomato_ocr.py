# 导包
from ascript.android import plug

plug.load("TomatoOcr:1.0.1")
from TomatoOcr import TomatoOcr

global tomatoOcr
def init_tomatoOcr():
    ocr = TomatoOcr()
    ocr.setContext(rec_type="ch-3.0")

    # 这里用了一个免费半年的 许可
    ocr.setLicense(
        "gAAAAABmPEIUAAAAAGchBoDtGyTGWXNtBCDTslF0i5dJnZ-AzQYjxuU2PqBsNZujr3utPCa4tnBCa1srVQw5vntwg-DucgQco-p4XA9_AWK9AsHguLHRm5vKeOaZKiO_8A==")

    ocr.setDetBoxType("rect")
    ocr.setDetUnclipRatio(1.9)
    ocr.setRecScoreThreshold(0.3)
    ocr.setReturnType("text")
    global tomatoOcr
    tomatoOcr = ocr

init_tomatoOcr()  # 初始化