import numpy as np
from load_arrays import*


class financial_analysis:
    c_c_Wac = 2.70  # capital costs($/W DC)
    o_m_Wac = 21  # O&M costs ($/kW DC)
    insur_c = .004  # insurance factor
    percent_downpayment = .1  # percentage of capital costs as downpayment
    m_i_r = .025  # mortgage interest rate
    insur_c = .004  # insurance factor
    loan_term = 30
    arr_fac_1 = np.array(
        [1 / (1 + .1) ** i for i in range(1, 31)]).reshape(-1, 1)
    arr_fac_2 = np.array(
        [1 / (1 + .03) ** i for i in range(1, 31)]).reshape(-1, 1)
    e_r = np.array(.0745)  # Electricity rate ($/kWh)
    s_deg = .01  # Assumed solar energy production degradation
    m_r = np.array([32.03, 88.27, 21.49]).reshape(3, 1, 1)  # millage rate
    f_ITC = .22  # federal income tax credit

    def __init__(self, arraypwr):
        self.arrayenergy = np.empty((1, 51, 361))
        for i in arraypwr:
            arrayenergy = np.load(f"{array(i).display}.npy")
            arrayenergy = arrayenergy.reshape(1, 51, 361)
            self.arrayenergy = np.vstack((self.arrayenergy, arrayenergy))
        self.arrayenergy = self.arrayenergy[1:, :, :]

    def capital_cost(self, array_power, level_of_subsidy=0):
        capitalcost = []
        for i in array_power:
            c_c = array(i).array * self.c_c_Wac * 1000
            capitalcost.append(c_c)
        self.capitalcost = (np.array(capitalcost).reshape(
            1, len(array_power))) * (1 - level_of_subsidy)
        self.down_p = self.capitalcost * self.percent_downpayment
        self.value = self.capitalcost - self.down_p
        self.array_pwr = array_power
        return self.capitalcost, self.down_p, self.value, self.array_pwr

    def _oper_cost(self, *array_power):
        o_c = []
        for i in self.array_pwr:
            oper_cost = array(i).array * self.o_m_Wac
            o_c.append(oper_cost)
        self.operationcosts = np.array(o_c).reshape(1, len(self.array_pwr))
        return self.operationcosts

    def _insurance_premium(self):
        self.insurance_premium = self.insur_c * self.capitalcost
        return self.insurance_premium

    def _mort_pay(self):
        self.mortgagepayment = (self.value * self.m_i_r * ((1 + self.m_i_r)
                                                           ** self.loan_term)) / (((1 + self.m_i_r)**self.loan_term) - 1)
        return self.mortgagepayment

    def _mortgage_interest(self):
        balance = self.value
        for i in range(0, 30):
            Future_value = self.value
            future_value_1 = balance[-1, :] * ((1 + self.m_i_r) ** 1)
            future_value_1 = future_value_1.reshape(1, 6)
            Future_value = np.append(Future_value, future_value_1, axis=0)
            Future_value = Future_value.reshape(-1, 6)
            current_bal = Future_value[-1, :] - self._mort_pay()
            balance = np.append(balance, current_bal, axis=0)
        balance = np.around(balance, 3)
        self.mortgageinterest = balance[:30, :] * self.m_i_r
        return self.mortgageinterest

    def pv_oper(self):
        self.paybackoper = np.dot(self.arr_fac_1, self._oper_cost())
        self.presentvalueoper = self.paybackoper.sum(axis=0).reshape(-1, 1)
        self.presentvalueoper_noi = np.sum(
            np.dot(self.arr_fac_2, self._oper_cost()), axis=0)
        return self.presentvalueoper, self.presentvalueoper_noi, self.paybackoper

    def pv_insurance(self):
        self.presentvalueinsurance = np.dot(
            self.arr_fac_1, self._insurance_premium())
        self.pwr_insurance = np.sum(self.presentvalueinsurance, axis=0)
        return self.pwr_insurance, self.presentvalueinsurance

    def pv_mortgage(self):
        self.presentvaluepayment = self._mort_pay() * self.arr_fac_1
        self.presentvaluepowerpayment = np.sum(
            self.presentvaluepayment, axis=0)
        self.mortgageinterestpayback = self._mortgage_interest() * self.arr_fac_1
        self.mortgageinterestpv = np.sum(self.mortgageinterestpayback, axis=0)
        return self.presentvaluepayment, self.presentvaluepowerpayment, self.mortgageinterestpv, self.mortgageinterestpayback

    def _energy_savings(self):
        deg_fac = np.arange(1, 31) * self.s_deg
        deg_fac = deg_fac.reshape(30, 1, 1, 1)
        self.energysavings = np.tile(self.arrayenergy.reshape(
            1, 6, 51, 361), (30, 1, 1, 1)) * (1 - deg_fac)
        self.pwr_energysavings = np.sum(self.energysavings, axis=0)
        return self.energysavings, self.pwr_energysavings

    def _util_sav(self):
        self.utilitysavings = self._energy_savings(
        )[0] * np.tile(self.e_r.reshape(1, 1, 1, 1), (30, 1, 1, 1))

        return self.utilitysavings

    def _pv_util_sav(self):
        x = self.arr_fac_1.reshape(30, 1, 1, 1)
        y = self.arr_fac_2.reshape(30, 1, 1, 1)
        self.util_sav = x * self._util_sav()
        self.presentvalueutilitysavings = (np.sum(self.util_sav, axis=0))
        self.util_sav_fornoi = np.sum((y * self._util_sav()), axis=0)
        return self.presentvalueutilitysavings, self.util_sav_fornoi, self.util_sav

    def _netoperatingincome(self):
        self.n_o_i = self._pv_util_sav(
        )[1] - self.presentvalueoper_noi.reshape(6, 1, 1)
        return self.n_o_i

    def _property_tax(self):
        local = (self.m_r[0, :, :] * self._netoperatingincome()) / 1000
        school = (self.m_r[1, :, :] * self._netoperatingincome()) / 1000
        county = (self.m_r[2, :, :] * self._netoperatingincome()) / 1000
        self.property_tax = local + school + county
        local_1 = self.m_r.reshape(-1, 1)[0, :] * self.capitalcost / 1000
        school_1 = self.m_r.reshape(-1, 1)[1, :] * self.capitalcost / 1000
        county_1 = self.m_r.reshape(-1, 1)[2, :] * self.capitalcost / 1000
        self.p_tax_installed_costs = local_1 + school_1 + county_1
        return self.property_tax, self.p_tax_installed_costs

    def _fed_inc_tax_benefit(self):
        self.federalincometax = self.f_ITC * self.capitalcost
        return self.federalincometax

    def pv_propertytax(self):
        self.propertytax1 = np.sum(
            np.dot(self.arr_fac_1.reshape(30, 1), self._property_tax()[1]), axis=0)
        self.propertytax2 = np.sum((self.arr_fac_1.reshape(
            30, 1, 1, 1) * self._property_tax()[0]), axis=0)
        return self.propertytax1, self.propertytax2

    def TLCC(self):
        self.TLCC_tax1 = self.down_p.T + self.pv_oper()[0] + self.pv_insurance()[0].reshape(
            6, 1) + self.pv_mortgage()[1].reshape(6, 1) + self.pv_propertytax()[0].reshape(6, 1)
        self.TLCC_tax2 = self.down_p.T.reshape(6, 1, 1) + self.pv_oper()[0].reshape(6, 1, 1) + self.pv_insurance()[
            0].reshape(6, 1, 1) + self.pv_mortgage()[1].reshape(6, 1, 1) + self.pv_propertytax()[1]
        return self.TLCC_tax1, self.TLCC_tax2

    def LCOE(self):
        self.LCOE1 = self.TLCC_tax1.reshape(
            6, 1, 1) / self._energy_savings()[1]
        self.LCOE2 = self.TLCC_tax2 / self._energy_savings()[1]
        return self.LCOE1, self.LCOE2

    def npv(self):
        self.npv_1 = self.pv_propertytax()[0].reshape(6, 1, 1) + self.pv_mortgage(
        )[2].reshape(6, 1, 1) - self.TLCC_tax1.reshape(6, 1, 1) + self._pv_util_sav()[0]
        self.npv_2 = self.pv_propertytax()[
            1] + self.pv_mortgage()[2].reshape(6, 1, 1) + self._pv_util_sav()[0] - self.TLCC_tax2
        return self.npv_1, self.npv_2

    # def payback(self):
    # 	costs = self.down_p.T
    # 	yr_br_up_costs = self.pv_oper()[2].T+self.pv_insurance()[1].T+self.pv_mortgage()[0].T
    # 	costs_8 = np.zeros_like(yr_br_up_costs)
    # 	yr_br_up_costs_1 = np.zeros_like(yr_br_up_costs[:,0])
    # 	for i in range(0,30):
    # 		yr_br_up_costs_1 += yr_br_up_costs[:,i]
    # 		costs_8[:,i] = yr_br_up_costs_1
    # 	costs = np.append(self.down_p.T, costs_8, axis =1)
    # 	costs = costs.reshape(6,31,1,1)
    # 	benefits_br = self.pv_mortgage()[3].T.reshape(6,30,1,1) + np.swapaxes(self._pv_util_sav()[2],0,1)
    # 	benefits_8 = np.zeros_like(benefits_br)
    # 	benefits_1 = np.zeros_like(benefits_br[:,0,:,:])
    # 	for j in range(0,30):
    # 		benefits_1 += benefits_br[:,i,:,:]
    # 		benefits_8[:,i,:,:] = benefits_1
    # 	benefits = np.append(np.zeros((6,1,51,361)), benefits_8, axis =1)
    # 	self.payback = - costs + benefits
    # 	return self.payback
