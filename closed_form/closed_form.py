from math import log, exp, sqrt
from scipy.stats import norm


def plainVanillaOption(s, k, r, q, v, t, optionType = 'Call'):
      if (optionType.upper()[0] == 'C'):
            style = 1
      else:
            style = -1    
      d1 = (log(s/k) + (r - q + v**2/2)*t) / (v*sqrt(t))
      d2 = d1 - v*sqrt(t)     
      if (t > 0):
            price = style * (s*exp(-q*t)*norm.cdf(style*d1) - k*exp(-r*t)*norm.cdf(style*d2))
      else:
            price = max(style * (s - k), 0)
      return(price)
      
################
# single barrier
# also see "The Complete Guide to Option Pricing Formulas" P.177 ~ P.180
################
def mu_(r, q, v):
      v2 = v**2
      return((r - q - v2/2)/v2)


def lambda_(r, q, v):
      return(sqrt(mu_(r, q, v)**2 + 2*r/v**2))
  
      
def z_(s, h, r, q, v, t):
      return(log(h/s)/v/sqrt(t) + lambda_(r, q, v)*v*sqrt(t))

      
def x1(s, k, r, q, v, t):
      return(log(s/k)/v/sqrt(t) + (mu_(r, q, v) + 1)*v*sqrt(t))

      
def x2(s, h, r, q, v, t):
      return(log(s/h)/v/sqrt(t) + (mu_(r, q, v) + 1)*v*sqrt(t))


def y1(s, k, r, q, v, t ,h):
      return(log(h**2/(s*k))/v/sqrt(t) + (mu_(r, q, v) + 1)*v*sqrt(t))


def y2(s, h, r, q, v, t):
      return(log(h/s)/v/sqrt(t) + (mu_(r, q, v) + 1)*v*sqrt(t))


def A1(s, k, r, q, v, t, phi):
      return(s*exp(-q*t)*norm.cdf(phi*x1(s, k, r, q, v, t)))


def B1(cash, s, k, r, q, v, t ,phi):
      return(cash*exp(-r*t) *
             norm.cdf(phi*x1(s, k, r, q, v, t) - phi*v*sqrt(t)))


def A2(s, h, r, q, v, t, phi):
      return(s*exp(-q*t)*norm.cdf(phi*x2(s, h, r, q, v, t)))


def B2(cash, s, h, r, q, v, t, phi):
      return(cash*exp(-r*t) *
             norm.cdf(phi*x2(s, h, r, q, v, t) - phi*v*sqrt(t)))
 
      
def A3(s, k, r, q, v, t, h, eta):
      return(s*exp(-q*t)*(h/s)**(2*mu_(r, q, v) + 2) *
             norm.cdf(eta*y1(s, k, r, q, v, t, h)))


def B3(cash, s, k, r, q, v, t, h, eta):
      return(cash*exp(-r*t)*(h/s)**(2*mu_(r, q, v)) * 
             norm.cdf(eta*y1(s, k, r, q, v, t, h) - eta*v*sqrt(t)))


def A4(s, h, r, q, v, t, eta):
      return(s*exp(-q*t)*(h/s)**(2*mu_(r, q, v) + 2) * 
             norm.cdf(eta*y2(s, h, r, q, v, t)))


def B4(cash, s, h, r, q, v, t, eta):
      return(cash*exp(-r*t)*(h/s)**(2*mu_(r, q, v)) * 
             norm.cdf(eta*y2(s, h, r, q, v, t) - eta*v*sqrt(t)))

      
def A5(cash, s, h, r, q, v, t, eta):
      mu_v = mu_(r, q, v)
      lambda_v = lambda_(r, q, v)
      z_v = z_(s, h, r, q, v, t)
      return(cash*((h/s)**(mu_v + lambda_v)*norm.cdf(eta*z_v) + 
                   (h/s)**(mu_v - lambda_v)*norm.cdf(eta*z_v - 2*eta*lambda_v*v*sqrt(t))))

    

def cashOrNothingAtHit(cash, s, h, r, q, v, t, 
                       knockInType = 'Down', isKnock = False):         
      if (t > 0 and not isKnock):
            if (knockInType.upper()[0] == 'D'):
                  if (s > h):
                        return(A5(cash, s, h, r, q, v, t, eta = 1))
                  else:
                        return(0)
            elif (knockInType.upper()[0] == 'U'):
                  if (s < h):
                        return(A5(cash, s, h, r, q, v, t, eta = -1))
                  else:
                        return(0)
            else:
                  return(0)
      elif (t >= 0 and isKnock):
            return(cash*exp(-r*t))
      else:
            return(0)
            

     
def assetOrNothingAtHit(s, h, r, q, v, t, 
                        knockInType = 'Down', isKnock = False):     
      if (t > 0 and not isKnock):
            cash = h
            if (knockInType.upper()[0] == 'D'):
                  if (s > h):
                        return(A5(cash, s, h, r, q, v, t, eta = 1))
                  else:
                        return(0)
            elif (knockInType.upper()[0] == 'U'):
                  if (s < h):
                        return(A5(cash, s, h, r, q, v, t, eta = -1))
                  else:
                        return(0)
            else:
                  return(0)
      elif (t >=0 and isKnock):
            return(s*exp(-r*t))
      else:
            return(0)
   
      
def cashOrNothingAtExpiry(cash, s, h, r, q, v, t,
                          knockType = 'DI', isKnock = False):     
      if (t > 0 and not isKnock):
            if (knockType.upper() == 'DI'):
                  if (s > h):
                        return(B2(cash, s, h, r, q, v, t, phi = -1) + 
                               B4(cash, s, h, r, q, v, t, eta = 1))
                  else:
                        return(0)
            elif (knockType.upper() == 'UI'):
                  if (s < h):
                        return(B2(cash, s, h, r, q, v, t, phi = 1) + 
                               B4(cash, s, h, r, q, v, t, eta = -1))
                  else:
                        return(0)
            elif (knockType.upper() == 'DO'):
                  if (s > h):
                        return(B2(cash, s, h, r, q, v, t, phi = 1) - 
                               B4(cash, s, h, r, q, v, t, eta = 1))
                  else:
                        return(0)
            elif (knockType.upper() == 'UO'):
                  if (s < h):
                        return(B2(cash, s, h, r, q, v, t, phi = -1) - 
                               B4(cash, s, h, r, q, v, t, eta = -1))
                  else:
                        return(0)
            else:
                  return(0)
      elif (t >= 0 and isKnock):
            if (knockType.upper()[1] == 'O'):
                  return(0)
            else:
                  return(cash*exp(-r*t))
      else:
            if (knockType.upper()[1] == 'O'):
                  return(cash)
            else:
                  return(0)

            

def assetOrNothingAtExpiry(s, h, r, q, v, t, 
                           knockType = 'DI', isKnock = False):
      if (t > 0 and not isKnock):
            if (knockType.upper() == 'DI'):
                  if (s > h):
                        return(A2(s, h, r, q, v, t, phi = -1) + 
                               A4(s, h, r, q, v, t, eta = 1))
                  else:
                        return(0)
            elif (knockType.upper() == 'UI'):
                  if (s < h):
                        return(A2(s, h, r, q, v, t, phi = 1) + 
                               A4(s, h, r, q, v, t, eta = -1))
                  else:
                        return(0)
            elif (knockType.upper() == 'DO'):
                  if (s > h):
                        return(A2(s, h, r, q, v, t, phi = 1) -
                               A4(s, h, r, q, v, t, eta = 1))
                  else:
                        return(0)
            elif (knockType.upper() == 'UO'):
                  if (s < h):
                        return(A2(s, h, r, q, v, t, phi = -1) -
                               A4(s, h, r, q, v, t, eta = -1))
                  else:
                        return(0)
            else:
                  return(0)
      elif (t >= 0 and isKnock):
            if (knockType.upper()[1] == 'O'):
                  return(0)
            else:
                  return(s*exp(-r*t))
      else:
            if (knockType.upper()[1] == 'O'):
                  return(s)
            else:
                  return(0)


def cashOrNothingOption(cash, s, k, h, r, q, v, t, 
                        knockType = 'DI', optionType = 'Call',
                        isKnock = False):
      if (t > 0 and not isKnock):
            if (knockType.upper() == 'DI' and optionType.upper()[0] == 'C'):
                  if (s > h):
                        if (k > h):
                              return(B3(cash, s, k, r, q, v, t, h, eta = 1))
                        else:
                              return(B1(cash, s, k, r, q, v, t ,phi = 1) - 
                                     B2(cash, s, h, r, q, v, t, phi = 1) + 
                                     B4(cash, s, h, r, q, v, t, eta = 1))
                  else:
                        return(0)
            elif (knockType.upper() == 'UI' and optionType.upper()[0] == 'C'):
                  if (s < h):
                        if (k > h):
                              return(B1(cash, s, k, r, q, v, t, phi = 1))
                        else:
                              return(B2(cash, s, h, r, q, v, t, phi = 1) - 
                                     B3(cash, s, k, r, q, v, t, h, eta = -1) + 
                                     B4(cash, s, h, r, q, v, t, eta = -1))
                  else:
                        return(0)
            elif (knockType.upper() == 'DI' and optionType.upper()[0] == 'P'):
                  if (s > h):
                        if (k > h):
                              return(B2(cash, s, h, r, q, v, t, phi = -1) - 
                                     B3(cash, s, k, r, q, v, t, h, eta = 1) + 
                                     B4(cash, s, h, r, q, v, t, eta = 1))
                        else:
                              return(B1(cash, s, k, r, q, v, t, phi = -1))
                  else:
                        return(0)
            elif (knockType.upper() == 'UI' and optionType.upper()[0] == 'P'):
                  if (s < h):
                        if (k > h):
                              return(B1(cash, s, k, r, q, v, t, phi = -1) -
                                     B2(cash, s, h, r, q, v, t, phi = -1) +
                                     B4(cash, s, h, r, q, v, t, eta = -1))
                        else:
                              return(B3(cash, s, k, r, q, v, t, h, eta = -1))
                  else:
                        return(0)
            elif (knockType.upper() == 'DO' and optionType.upper()[0] == 'C'):
                  if (s > h):
                        if (k > h):
                              return(B1(cash, s, k, r, q, v, t, phi = 1) -
                                     B3(cash, s, k, r, q, v, t, h, eta = 1))
                        else:
                              return(B2(cash, s, h, r, q, v, t, phi = 1) -
                                     B4(cash, s, h, r, q, v, t, eta = 1))
                  else:
                        return(0)
            elif (knockType.upper() == 'UO' and optionType.upper()[0] == 'C'):
                  if (s < h):
                        if (k > h):
                              return(0)
                        else:
                              return(B1(cash, s, k, r, q, v, t, phi = 1) -
                                     B2(cash, s, h, r, q, v, t, phi = 1) +
                                     B3(cash, s, k, r, q, v, t, h, eta = -1) - 
                                     B4(cash, s, h, r, q, v, t, eta = -1))
                  else:
                        return(0)
            elif (knockType.upper() == 'DO' and optionType.upper()[0] == 'P'):
                  if (s > k):
                        if (k > h):
                              return(B1(cash, s, k, r, q, v, t, phi = -1) -
                                     B2(cash, s, h, r, q, v, t, phi = -1) +
                                     B3(cash, s, k, r, q, v, t, h, eta = 1) - 
                                     B4(cash, s, h, r, q, v, t, eta = 1))
                        else:
                              return(0)
                  else:
                        return(0)
            elif (knockType.upper() == 'UO' and optionType.upper()[0] == 'P'):
                  if (s < h):
                        if (k > h):
                              return(B2(cash, s, h, r, q, v, t, phi = -1) -
                                     B4(cash, s, h, r, q, v, t, eta = -1))
                        else:
                              return(B1(cash, s, k, r, q, v, t, phi = -1) -
                                     B3(cash, s, k, r, q, v, t, h, eta = -1))
                  else:
                        return(0)
            else:
                  return(0)
      elif (t > 0 and isKnock):
            if (knockType.upper()[1] == 'I'):
                  if (optionType.upper()[0] == 'P'):
                        style = -1
                  else:
                        style = 1
            
                  d = (log(s/k)-(r - q - v**2/2)*t) / (v*sqrt(t))
                  return(cash*exp(-r*t)*norm.cdf(style*d)) # cash or nothing option
            else:
                  return(0)
      else:
            if ((isKnock and knockType.upper()[1] == 'I') or
                (not isKnock and knockType.upper()[1] == 'O')):
                  return(cash)
            else:
                  return(0)
      
      

def assetOrNothingOption(s, k, h, r, q, v, t, 
                         knockType = 'DI', optionType = 'Call', 
                         isKnock = False):
      if (t > 0 and not isKnock):
            if (knockType.upper() == 'DI' and optionType.upper()[0] == 'C'):
                  if (s > h):
                        if (k > h):
                              return(A3(s, k, r, q, v, t, h, eta = 1))
                        else:
                              return(A1(s, k, r, q, v, t, phi = 1) -
                                     A2(s, h, r, q, v, t, phi = 1) +
                                     A4(s, h, r, q, v, t, eta = 1))
                  else:
                        return(0)
            elif (knockType.upper() == 'UI' and optionType.upper()[0] == 'C'):
                  if (s < h):
                        if (k > h):
                              return(A1(s, k, r, q, v, t, phi = 1))
                        else:
                              return(A2(s, h, r, q, v, t, phi = 1) -
                                     A3(s, k, r, q, v, t, h, eta = -1) + 
                                     A4(s, h, r, q, v, t, eta = -1))
                  else:
                        return(0)
            elif (knockType.upper() == 'DI' and optionType.upper()[0] == 'P'):
                  if (s > h):
                        if (k > h):
                              return(A2(s, h, r, q, v, t, phi = -1) -
                                     A3(s, k, r, q, v, t, h, eta = 1) + 
                                     A4(s, h, r, q, v, t, eta = 1))
                        else:
                              return(A1(s, k, r, q, v, t, phi = -1))
                  else:
                        return(0)
            elif (knockType.upper() == 'UI' and optionType.upper()[0] == 'P'):
                  if (s < h):
                        if (k > h):
                              return(A1(s, k, r, q, v, t, phi = -1) - 
                                     A2(s, h, r, q, v, t, phi = -1) +
                                     A3(s, k, r, q, v, t, h, eta = -1))
                        else:
                              return(A3(s, k, r, q, v, t, h, eta = -1))
                  else:
                        return(0)
            elif (knockType.upper() == 'DO' and optionType.upper()[0] == 'C'):
                  if (s > h):
                        if (k > h):
                              return(A1(s, k, r, q, v, t, phi = 1) - 
                                     A3(s, k, r, q, v, t, h, eta = 1))
                        else:
                              return(A2(s, h, r, q, v, t, phi = 1) -
                                     A4(s, h, r, q, v, t, eta = 1))
                  else:
                        return(0)
            elif (knockType.upper() == 'UO' and optionType.upper()[0] == 'C'):
                  if (s < h):
                        if (k > h):
                              return(0)
                        else:
                              return(A1(s, k, r, q, v, t, phi = 1) -
                                     A2(s, h, r, q, v, t, phi = 1) +
                                     A3(s, k, r, q, v, t, h, eta = -1) - 
                                     A4(s, h, r, q, v, t, eta = -1))
                  else:
                        return(0)
            elif (knockType.upper() == 'DO' and optionType.upper()[0] == 'P'):
                  if (s > h):
                        if (k > h):
                              return(A1(s, k, r, q, v, t, phi = -1) -
                                     A2(s, h, r, q, v, t, phi = -1) +
                                     A3(s, k, r, q, v, t, h, eta = 1) - 
                                     A4(s, h, r, q, v, t, eta = 1))
                        else:
                              return(0)
                  else:
                        return(0)
            elif (knockType.upper() == 'UO' and optionType.upper()[0] == 'P'):
                  if (s < h):
                        if (k > h):
                              return(A2(s, h, r, q, v, t, phi = -1) - 
                                     A4(s, h, r, q, v, t, eta = -1))
                        else:
                              return(A1(s, k, r, q, v, t, phi = -1) -
                                     A3(s, k, r, q, v, t, h, eta = -1))
                  else:
                        return(0)
            else:
                  return(0)
      elif (t > 0 and isKnock):
            if (knockType.upper()[1] == 'I'):
                  if (optionType.upper()[0] == 'P'):
                        style = -1
                  else:
                        style = 1
            
                  d = (log(s/k)-(r - q + v**2/2)*t) / (v*sqrt(t))
                  return(s*exp(-q*t)*norm.cdf(style*d)) # asset or nothing option
            else:
                  return(0)
      else:
            if ((isKnock and knockType.upper()[1] == 'I') or
                (not isKnock and knockType.upper()[1] == 'O')):
                  return(s)
            else:
                  return(0)                  
