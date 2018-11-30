import emdee

def run_tests():
    testEmdee = emdee.Emdee(mode='new')
    print()

    testEmdee.AddParam('core_mass')
    testEmdee.AddParam('Qimp',[1.0,4.0])
    testEmdee.PrintParams()
    testEmdee.AddParam('core_mass',[1.5,1.6])
    print()

    testEmdee.ChangeBounds('core_mass',[1.6,2.1])
    testEmdee.PrintParams()
    testEmdee.ChangeBounds('core_radius',[9.0,9.2])
    print()

    print(testEmdee.nwalkers)
    testEmdee.ChangeWalkers(30)
    print(testEmdee.nwalkers)
    testEmdee.ChangeWalkers(17)
    testEmdee.ChangeWalkers(2)
    print(testEmdee.nwalkers)
    print()

    print(testEmdee.dstar_dir)
    testEmdee.ChangeDStarDir('some/dstar/somewhere')
    print(testEmdee.dstar_dir)
    print()


if __name__ == '__main__':
    run_tests()