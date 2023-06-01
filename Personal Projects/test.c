#include <stdio.h>

int f(int n, int a, int b) {
    if (n == 0)
        return 0;
    if (a > n % 10)
        a = n % 10;
    if (b < n % 10)
        b = n % 10;
    return b - a + f(n/10, a, b);
}

int main() {
    printf("%d\n", f(214354322, 10, -1));
    return 0;
}
