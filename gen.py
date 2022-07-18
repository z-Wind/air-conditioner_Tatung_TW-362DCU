def 開關(x):
    return int(x)
    
def 機能(x):
    if x == "冷氣":
        return 0b100
    elif x == "暖氣":
        return 0b001
    elif x == "除濕":
        return 0b010
    elif x == "自動":
        return 0b000
    elif x == "送風":
        return 0b110
    else:
        raise f"機能:{x} 不支援"
        
def 韻律(x):
    return int(x)
    
def 睡眠(x):
    return int(x)
	
def 定時(x):
    if x == "取消":
        return 0b01000
    elif x == "0.5":
        return 0b11111
    
    try:
        rev = f"{int(x, 10):04b}"[::-1]
        return 0b10000 + int(rev, 2)
    except ValueError:
        raise f"定時:{x} 不支援"
        
def Fuzzy(x):
    if x == "冷":
        return 0b10
    elif x == "適":
        return 0b01
    elif x == "熱":
        return 0b11
    else:
        raise f"Fuzzy:{x} 不支援"
        
def 殺菌(x):
    return int(x)
    
def 風速(x):
    if x == "弱":
        return 0b100
    elif x == "中":
        return 0b010
    elif x == "強":
        return 0b001
    elif x == "自動":
        return 0b000
    else:
        raise f"風速:{x} 不支援"
		
def 溫度(x):
    if not 17 <= x <= 30:
        raise f"溫度:{x} 不支援"
        
    return int(f"{x-16:04b}"[::-1], 2)
    
def gencode(config):
    code_開關 = 開關(config["開關"])
    code_機能 = 機能(config["機能"])
    code_韻律 = 韻律(config["韻律"])
    code_睡眠 = 睡眠(config["睡眠"])
    code_定時 = 定時(config["定時"])
    code_Fuzzy = Fuzzy(config["Fuzzy"])
    code_殺菌 = 殺菌(config["殺菌"])
    code_風速 = 風速(config["風速"])
    code_溫度 = 溫度(config["溫度"])
    
    code = f"{code_開關:01b}1{code_機能:03b}0{code_韻律:01b}{code_睡眠:01b}0{code_定時:05b}{code_Fuzzy:02b}00{code_殺菌:01b}111{code_風速:03b}{code_溫度:04b}1"
    
    assert len(code) == 30
    return int(code, 2)

def gen_irplus(code, config):
    str = ""
    str += '<irplus>\n'
    str += ' <device manufacturer="Tatung" model="TW-362DCU" columns="20" format="WINLIRC_SPACEENC" one-pulse="650" one-space="1750" zero-pulse="650" zero-space="550" header-pulse="3650" header-space="2350" gap-space="8900" gap-pulse="650" bits="30" pre-bits="1"  toggle-bit-pos="" repeat="2">\n'
    str += f'  <button label="指令" labelSize="25.0" span="8">0x0 0x{code:08X}</button>\n'
    str += '\n'
    str += f'  <button label="設定" labelSize="25.0" span="20" backgroundColor="00444444"> </button>\n'
    show = lambda k,v:f'  <button label="{k}={v}" labelSize="25.0" span="20" backgroundColor="00444444"> </button>\n'
    for k,v in config.items():
        if k == "開關":
            continue
        str += show(k,v)

    str += ' </device>\n'
    str += '</irplus>\n'
    
    return str

if __name__ == '__main__':
    config = {
        "開關": True,
        "機能": "冷氣",
        "韻律": True,
        "睡眠": False,
        "定時": "取消",
        "Fuzzy": "適",
        "殺菌": True,
        "風速": "自動",
        "溫度": 29,
    }
    
    code = gencode(config)
    print(f"0b{code:030b}")
    print(f"0x0 0x{code:08X}")
    
    str = gen_irplus(code, config)
    print(str)
    with open("cmd.irplus", "w") as f:
        f.write(str)
    