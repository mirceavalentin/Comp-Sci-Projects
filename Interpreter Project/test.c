#include <stdio.h>

int main() {

    enum Company { GOOGLE, FACEBOOK, XEROX, YAHOO, EBAY, MICROSOFT };

    enum Company firstCompany = XEROX;
    printf("First company is: %d\n", firstCompany);

    enum Company secondCompany = GOOGLE;
    printf("Second company is: %d\n", secondCompany);

    enum Company thirdCompany = EBAY;
    printf("Third company is: %d\n", thirdCompany);

    return 0;
}