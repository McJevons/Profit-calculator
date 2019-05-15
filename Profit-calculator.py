#!/usr/bin/env python
# coding: utf-8

# In[1]:


from decimal import Decimal, ROUND_HALF_UP


# In[124]:


def round_dec(n, d=2):
    '''
    对输入的n做四舍五入运算，并输出结果
    args:
        n:需要四舍五入的数字
        d:保留小数位数，默认=2
    -----------------
    return:
        返回Decimal格式的结果
    '''
    s = '0.'
    for x in range(d):
        s += '0'
    n = Decimal(n)
    return n.quantize(Decimal(s), rounding=ROUND_HALF_UP)


# ## 等额本金
# 每月还款额Fm=每月还款本金+每月还款利息。Pm+Rm
# 
# 每月还款本金Pm=贷款总额/贷款月数 P/M。
# 
# 每月还款利息Rm=贷款本金余额 * 贷款月利率 Pb * i（ 贷款月利率=年利率/12）。
# 
# 贷款本金余额Pb=贷款总额-已还款月数 * 每月还款本金 P-m * Pm

# In[134]:


def average_capital(P, I, M):
    '''
    等额本金
    返回一个包含每月返款数据元组的迭代器
    '''
    Pm = Decimal(P) / M  # 每月返本金，每月相等
    i = Decimal(I) / 12  # 月利率
    for m in range(M):
        Pb = P - m * Pm  # 月初本金余额
        Rm = Pb * i  # 每月返收益
        Fm = Pm + Rm  # 每月返款额
        Pe = Pb - Pm  # 月末本金余额
        result = (m + 1, Fm, Pm, Rm, Pb, Pe)
        yield result


# ## 等额本息
# 本月还息=本月余额×月利率
# 
# 本月还本=每月还款额-本月还息
# 
# 每月还款额=[贷款本金×月利率×（1+月利率）^还款月数]÷[（1+月利率）^还款月数－1]

# In[135]:


def average_capital_plus_interest(P, I, M):
    '''
    等额本息
    返回一个包含每月返款数据元组的迭代器
    '''
    P = Decimal(P)
    i = Decimal(I) / 12  # 月利率
    result = ()
    Fm = P * i * ((1 + i)**M) / (((1 + i)**M) - 1)  # 每月返款额，每月相等
    for m in range(M):
        if not result:  # 此处result为上月数据
            Pb = P  # 月初余额，若上月数据不存在则为首月，月初余额为本金
        else:
            Pb = result[-1]  # 月初余额，为上月月末余额
        Rm = Pb * i  # 还息
        Pm = Fm - Rm  # 还本
        Pe = Pb - Pm  # 月末余额
        result = (m + 1, Fm, Pm, Rm, Pb, Pe)
        yield result


# In[127]:


def calculate(P, I, M, func, detail=True):
    '''
    计算并输出投资收益结果
    args:
        P:投资金额
        I:年收益率
        M:投资期数（月）
        func:投资模式:
                "ac":等额本金
                "acpi":等额本息
        detail:boolean,是否打印每期明细
    ----------------------------
    return:None
    '''
    func_dict = {'ac': average_capital, 'acpi': average_capital_plus_interest}
    f = func_dict[func]
    F = Decimal(0)
    R = Decimal(0)
    for r in f(P, I, M):
        F += r[1]
        R += r[3]
        r = r[0:1] + tuple(map(round_dec, r[1:]))  # 对元组中数字部分四舍五入
        if detail: print('第%d月返款额：%s，返本金：%s，返收益，%s，月初本金余额：%s，月末本金余额：%s' % r)
    print('返款总额：%s，收益总计：%s' % (round_dec(F), round_dec(R)))


# In[142]:


calculate(10000000, 0.05, 60, 'acpi', False)


# In[143]:


calculate(10000000, 0.05, 60, 'ac', False)


# ## 等额本息-复投同利率等额本息 

# In[39]:


def bxft(M, P, I, m=0, G=0):
    i = I / 12
    Fm = P * i * ((1 + i)**(M - m)) / (((1 + i)**(M - m)) - 1)
    # print('第%s月投资金额：%s，投资单期回款：%s，投资期末收益：%s' % (m+1, P, Fm, Fm*(M-m)-P))
    G = G + Fm * (M - m) - P
    m += 1
    if m < M and m > 1:
        return bxft(M, Fm + P, I, m, G)
    elif m <= 1:
        return bxft(M, Fm, I, m, G)

    # print('最终收益：%s' % G)
    return G


# In[40]:


bxft(6, 10000, 0.085)


# ## 收益分析 

# In[41]:


G = []
for m in np.arange(3, 37, 3):
    G.append(bxft(M=m, I=0.085, P=10000))


# In[42]:


data = pd.DataFrame({'期数': np.arange(3, 37, 3), '收益': G})
data


# In[43]:


data['最终收益率'] = data['收益'] / 10000


# In[44]:


data['年化收益率'] = (12 / data['期数']) * data['收益'] / 10000


# In[ ]:




