package objects;

import java.io.Serializable;

public class TestObjMain implements Evaluatable, Serializable {
    int a;
    double b;
    String c;

    public TestObjMain() {
        a = 2; b = 3.14; c = "cde";
    }
}