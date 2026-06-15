from pyats import aetest


class MyTest(aetest.Testcase):
  @aetest.test
  def sample_test(self):
    print("my first test with aetest")



if __name__== "__main__":
  aetest.main()
