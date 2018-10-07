import pandas as pd
import numpy as np


def IsPtInPoly(sPoint, pointList):
    aLon, aLat = sPoint[0], sPoint[1]
    iSum = 0
    iCount = len(pointList)

    if (iCount < 3):
        return False

    for i in range(iCount):

        pLon1 = pointList[i][0]
        pLat1 = pointList[i][1]

        if (i == iCount - 1):

            pLon2 = pointList[0][0]
            pLat2 = pointList[0][1]
        else:
            pLon2 = pointList[i + 1][0]
            pLat2 = pointList[i + 1][1]

        if ((aLat >= pLat1) and (aLat < pLat2)) or ((aLat >= pLat2) and (aLat < pLat1)):

            if (abs(pLat1 - pLat2) > 0):

                pLon = pLon1 - ((pLon1 - pLon2) * (pLat1 - aLat)) / (pLat1 - pLat2);

                if (pLon < aLon):
                    iSum += 1

    if (iSum % 2 != 0):
        return True
    else:
        return False


dsPoints = pd.read_excel("/Users/wanghaoyi/Desktop/D2N/CONSADDRwithLLGaode.xls")
dsPoints["TZ"] = ""

# IsPtInPoly(0.5, 0.5, [[1, 1], [1, -1], [-1, -1], [-1, 1]])

# --
# Load TZ Data
# --
dsTZ = pd.read_excel("/Users/wanghaoyi/Desktop/D2N/TradeZone.xlsx")

TZList = dsTZ["SHAPE ID"].unique()
TZDic = {}

# Create TZ Coordinate Dictionary
for TZ in TZList:
    # TZ = "NANJINGEAST"
    TZtemp = dsTZ[dsTZ["SHAPE ID"] == TZ][["LATITUDE", "LONGITUDE"]]

    # Convert from Dataframe to Array
    TZArray = np.array(TZtemp).tolist()

    TZDic[TZ] = TZArray

# Update TZ against the address
for indexs in dsPoints.index:

    sPoint = list(dsPoints.loc[indexs][["lat", "lng"]])

    for key in TZDic:
        if IsPtInPoly(sPoint, TZDic[key]):
            dsPoints.iloc[indexs, 6] = key


dsPoints.to_excel("/Users/wanghaoyi/Desktop/D2N/CONSADDRwithLLGaode.xls")
