def true(*exprs):
    return True

def mll(*exprs):
    if len(exprs) == 0:
        return
    return exprs[-1]