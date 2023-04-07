#include <stdio.h>

// SALARY CALCULATOR
// The user inputs the hours worked.
// The program should output the gross pay, the taxes paid and the net pay.
// The basic pay rate is 12.00$/hr. Overtime is excess of >40 hours which is 18$/hr
// The tax rate is: first 300$ is taxed at 15%, extra 150$ is taxed at 20%, everything extra on top of that is taxed at 25%

int main() {

    printf("This program calculates your gross pay, taxes and net pay based on the hours you've worked.\n");
    printf("Enter the number of hours you've worked: ");

    int hours_worked = 0;
    int overtime_hours = 0;
    float gross_pay = 0.00;
    float tax = 0;
    float net_pay = 0;

    scanf("%d", &hours_worked);

    if(hours_worked > 40){
        overtime_hours = hours_worked - 40;
        hours_worked = hours_worked - overtime_hours;
        gross_pay = (overtime_hours * 18.00) + (hours_worked * 12.00);
        printf("Your gross pay is: %.2f$\n", gross_pay);
            // Case 1: The salary is under <=300 so the tax is 15%.
            if(gross_pay <= 300){
                tax = (15 * gross_pay) / 100;
                net_pay = gross_pay - tax;
                printf("The taxes you've paid are: %.2f$. Therefore, your net salary is: %.2f$\n", tax, net_pay);
            }
            // Case 2: The salary is over 300 and under 450 so the tax is 15% and 20%.
            else{
                if(gross_pay <= 450){
                    int second_tax_bracket = 0;
                    int first_tax_bracket = 0;
                    second_tax_bracket = gross_pay - 300.00;
                    first_tax_bracket = gross_pay - second_tax_bracket;
                    tax = ((15 * first_tax_bracket) / 100) + ((20 * second_tax_bracket) / 100);
                    net_pay = gross_pay - tax;
                    printf("The taxes you've paid are: %.2f$. Therefore, your net salary is: %.2f$\n", tax, net_pay);
                }
                // Case 3: The salary is over 450 so the tax is 15%, 20% and 25%.
                else{
                    int second_tax_bracket = 0;
                    int first_tax_bracket = 0;
                    int third_tax_bracket = 0;
                    third_tax_bracket = gross_pay - 450;
                    second_tax_bracket = (gross_pay - third_tax_bracket) - 300.00;
                    first_tax_bracket = gross_pay - (second_tax_bracket + third_tax_bracket);
                    tax = ((15 * first_tax_bracket) / 100) + ((20 * second_tax_bracket) / 100) + ((25 * third_tax_bracket) / 100);
                    net_pay = gross_pay - tax;
                    printf("The taxes you've paid are: %.2f$. Therefore, your net salary is: %.2f$\n", tax, net_pay);
                }
            }
        }
    // There are no extra hours worked.
    else{
        gross_pay = (hours_worked * 12.00);
        printf("Your gross pay is: %.2f$\n", gross_pay);
            // Case 1: The salary is under <=300 so the tax is 15%.
            if(gross_pay <= 300){
            tax = (15 * gross_pay) / 100;
            net_pay = gross_pay - tax;
            printf("The taxes you've paid are: %.2f$. Therefore, your net salary is: %.2f$\n", tax, net_pay);
            }
            // Case 2: The salary is over 300 and under 450 so the tax is 15% and 20%.
            else{
                if(gross_pay <= 450){
                    int second_tax_bracket = 0;
                    int first_tax_bracket = 0;
                    second_tax_bracket = gross_pay - 300.00;
                    first_tax_bracket = gross_pay - second_tax_bracket;
                    tax = ((15 * first_tax_bracket) / 100) + ((20 * second_tax_bracket) / 100);
                    net_pay = gross_pay - tax;
                    printf("The taxes you've paid are: %.2f$. Therefore, your net salary is: %.2f$\n", tax, net_pay);
                }
                // Case 3: The salary is over 450 so the tax is 15%, 20% and 25%.
                else{
                    int second_tax_bracket = 0;
                    int first_tax_bracket = 0;
                    int third_tax_bracket = 0;
                    third_tax_bracket = gross_pay - 450;
                    second_tax_bracket = (gross_pay - third_tax_bracket) - 300.00;
                    first_tax_bracket = gross_pay - (second_tax_bracket + third_tax_bracket);
                    tax = ((15 * first_tax_bracket) / 100) + ((20 * second_tax_bracket) / 100) + ((25 * third_tax_bracket) / 100);
                    net_pay = gross_pay - tax;
                    printf("The taxes you've paid are: %.2f$. Therefore, your net salary is: %.2f$\n", tax, net_pay);
                }
            }
    }

    return 0;
}