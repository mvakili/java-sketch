class Base {
    public int x;
    static int y;
    public void foo() {
        this.x = 0;
    }
    void a() {
	y = 0;
    }
}

class Ext extends Base {
    int y;
    public Ext (int x) {
        // super(x);
        this.x = this.x + 1;
    }

    @Override
    public void foo() {
	this.x = 0;
        // super.foo();
        // super.foo();
    }
}

class Test {
    harness static void test (int x) {
        Base b = new Base(x);
        Ext e = new Ext(x);
    }
}
