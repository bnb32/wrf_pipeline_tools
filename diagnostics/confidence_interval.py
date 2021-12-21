import numpy as np

def r_bound(z):
    return (np.exp(2*z)-1)/(np.exp(2*z)+1)

def conInterval(val,samples):
    tmp=1/np.sqrt(samples-3)
    z_val = 0.5*np.log((1+val)/(1-val))
    z_upper_90=z_val+tmp*1.645
    z_lower_90=z_val-tmp*1.645

    z_upper_85=z_val+tmp*1.44
    z_lower_85=z_val-tmp*1.44

    z_upper_80=z_val+tmp*1.282
    z_lower_80=z_val-tmp*1.282
    
    return [
            r_bound(z_lower_90),r_bound(z_upper_90),
            r_bound(z_lower_85),r_bound(z_upper_85),
            r_bound(z_lower_80),r_bound(z_upper_80)]
