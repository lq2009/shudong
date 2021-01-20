from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    uid: Optional[str] = None
    name: Optional[str] = None
    pic: Optional[str] = None
    site: Optional[str] = None
    login: bool = False
    sysop: bool = False
    
class NickName:
    pre = '路人'
    next = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','秋','冬',
    '甲','乙','丙','丁','戊','己','庚','辛','壬','癸','子','丒','寅','卯','辰','巳','午','未','申','酉','戌','亥','吘','尤',
    '张','孙','王','金','炎','焉','宫','商','角','徵','羽','安','沧','婵','泊','澈','辰','桢','澄','楚','蜀','巴','雷','风',
    '秦','燕','赵','钱','渝','诺','冉','芮','筱','宁','沪','苏','沽','余','藏','姜','允','珰','圩','伶','泽','电','春','夏']