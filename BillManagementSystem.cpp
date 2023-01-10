#include <iostream>
#include <process.h>
#include <fstream>
#include <stdlib.h>
#include <cmath>
#include <conio.h>
#include <iomanip>
#include <string>
#include <sstream>
#include <math.h>
#include <cstring>
#include <bits/stdc++.h>
using namespace std;

string StaffName;

class LoginManager /*: virtual public Bill*/
{
public:
    int usrID;
    string staffNameBill;
    LoginManager()
    {
        accessGranted = 0;
    }
    void login()
    {
        cout << "\n\t\t\t\t Staff Login:";
        cout << "\n\n\t\t\t User name: ";
        cin >> userNameAttempt;

        usrID = checkFile(userNameAttempt, "users.dat");
        if (usrID != 0)
        {
            cout << "\t\t\t Password: ";
            cin >> passwordAttempt;

            int pwdID = checkFile(passwordAttempt, "pswds.dat");
            if (usrID == pwdID) // ID check
            {
                int staffID = usrID;
                cout << "\n\t\t\t\t Welcome Staff";
                cout << "\n\t\t\t\t Staff ID  : " << staffID;
                cout << "\n\t\t\t\t Staff Name: " << getName(staffID, "staffname.dat");
                cout << "\n\n\n\t\t\t Logged In Successfully!\n";
                ::StaffName = getName(staffID, "staffname.dat");

                return;
            }
            else
            {
                cout << "\n\t\t\t Wrong password.\n\t\t\t Try again...\n"
                     << endl;
                login();
            }
        }
        else
        {
            cout << "\n\t\t\t Wrong User Name.\n\t\t\t Try again...\n"
                 << endl;
            login();
        }
    }

    void addUser(const string name, const string username, const string password)
    {
        if (checkFile(username, "users.dat") != 0)
        {
            cout << "That username is not availble." << endl;
            return;
        }

        int id = 1 + getLastID();
        saveFile(username, "users.dat", id);
        saveFile(password, "pswds.dat", id);
        saveNameFile(name, "staffname.dat", id);
    }

    int getLastID()
    {
        fstream file;
        file.open("users.dat", ios::in);
        file.seekg(0, ios::end);

        if (file.tellg() == -1)
            return 0;

        string s;

        for (int i = -1; s.find("#") == string::npos; i--)
        {
            file.seekg(i, ios::end);
            file >> s;
        }

        file.close();
        s.erase(0, 4);

        int id;
        istringstream(s) >> id;

        return id;
    }
    string getName(int Idstf, const char *s_fileName)
    {
        ifstream staffn;
        string nline;
        int sid = Idstf;
        int line_no;
        int current_line = 0;

        stringstream stream;
        stream << sid;
        string poststrid;
        stream >> poststrid;
        string prevstrid = "#ID:";

        string strid = prevstrid + poststrid;

        staffn.open(s_fileName);
        while (!staffn.eof())
        {
            current_line++;
            getline(staffn, nline);
            if (nline == strid)
            {
                break;
            }
        }
        for (int i = 1; i <= current_line; i++)
        {
            if (i = current_line - 1)
            {
                getline(staffn, nline);
                return nline;
                break;
            }
        }
    }

    int checkFile(string attempt, const char *p_fileName)
    {
        string line;
        fstream file;

        string currentChar;
        long long eChar;

        file.open(p_fileName, ios::in);

        while (1)
        {
            file >> currentChar;
            if (currentChar.find("#ID:") != string::npos)
            {
                if (attempt == line)
                {
                    file.close();
                    currentChar.erase(0, 4);
                    int id;
                    istringstream(currentChar) >> id;
                    return id;
                }
                else
                {
                    line.erase(line.begin(), line.end());
                }
            }
            else
            {
                istringstream(currentChar) >> eChar;
                line += (char)decrypt(eChar);
                currentChar = "";
            }

            if (file.peek() == EOF)
            {
                file.close();
                return 0;
            }
        }
    }

    void saveNameFile(string p_line, const char *p_fileName, const int &id)
    {
        fstream nfile;
        nfile.open(p_fileName, ios::app);
        nfile.seekg(0, ios::end);

        if (nfile.tellg() != 0)
            nfile << "\n";

        nfile.seekg(0, ios::beg);

        nfile << "#ID:" << id;
        nfile << "\n"
              << p_line;
        nfile.close();
    }

    void saveFile(string p_line, const char *p_fileName, const int &id)
    {
        fstream file;
        file.open(p_fileName, ios::app);
        file.seekg(0, ios::end);

        if (file.tellg() != 0)
            file << "\n";

        file.seekg(0, ios::beg);

        for (int i = 0; i < p_line.length(); i++)
        {
            file << encrypt(p_line[i]);
            file << "\n";
        }

        file << "#ID:" << id;
        file.close();
    }

    long long encrypt(int p_letter)
    {
        return powf(p_letter, 5) * 4 - 14;
    }
    int decrypt(long long p_letter)
    {
        return powf((p_letter + 14) / 4, 1 / 5.f);
    }

private:
    string userNameAttempt;
    string passwordAttempt;
    bool accessGranted;
};

class Bill : public LoginManager
{
    char Iname[50][50];
    // string  Iname;

public:
    int totalItems;
    float qty[3];
    float price[3];
    float vatprice[3];
    int tprice[3];
    void input();
    void output1();
};

// Defining Fuctions of class

void Bill::input()
{
    system("CLS");
    cout << "\nEnter number of items: ";
    cin >> totalItems;

    for (int i = 0; i < totalItems; i++)
    {
        cout << "Enter name of Iteam " << i + 1 << ": ";
        cin >> Iname[i];
        cout << "Enter quantity: ";
        cin >> qty[i];
        cout << "Enter price of item " << i + 1 << ": ";
        cin >> price[i];
        tprice[i] = qty[i] * price[i];
        cout << endl;
        system("PAUSE");
        system("CLS");
    }
}

void Bill ::output1()
{
    int a;
    time_t t = time(0); // get time now
    tm *now = localtime(&t);
    // LoginManager name;
    string staff = ::StaffName;
    // Time
    time_t time_ptr;
    time_ptr = time(NULL);
    tm *tm_local = localtime(&time_ptr);


    ifstream infile("COUNT.TXT");
    infile >> a;

    ofstream outfile("COUNT.TXT");
    a += 1;
    outfile << a;
    outfile.close();
    {
        ofstream outfile("Bill_Book.TXT", ios::app);
        outfile << endl
                << "\nBill No.: " << a << endl;
        outfile << "==============================================================================\n";
        outfile << "  Date : " << now->tm_mday << '/' << (now->tm_mon + 1) << '/' << (now->tm_year + 1900) << endl;
        outfile << "  Time : " << tm_local->tm_hour << ":" << tm_local->tm_min << ":" << tm_local->tm_sec << endl;
        outfile << "  Staff: " << staff << endl;
        outfile << "------------------------------------------------------------------------------\n";
        outfile << " Description  \t\tQty\t\tUnit Rate\t\t   Amount";
        outfile << "\n==============================================================================\n";

        cout << "\n------------------------------------------------------------------------------\n";
        cout << "|                               AM Retail                                    |\n";
        cout << "|                          Mohanty Pvt. Limited.                             |\n";
        cout << "|                         GST No. : 564AAABY56E2                             |\n";
        cout << "==============================================================================\n";
        cout << "  Date:  " << now->tm_mday << '/' << (now->tm_mon + 1) << '/' << (now->tm_year + 1900) << "\n";
        cout << "  Time:  " << tm_local->tm_hour << ":" << tm_local->tm_min << ":" << tm_local->tm_sec << endl;
        cout << "  Staff: " << staff << endl;
        cout << "------------------------------------------------------------------------------\n";
        cout << " Description  \t\tQty\t\tUnit Rate\t\t   Amount";
        cout << "\n==============================================================================\n";
        for (int i = 0; i < totalItems; i++)
        {
            outfile << left << setw(15) << Iname[i] << "\t\t" << right << setw(3) << qty[i] << "\t\t" << right << setw(8) << price[i] << " \t\t" << right << setw(9) << tprice[i] << endl;
            cout << left << setw(15) << Iname[i] << "\t\t" << right << setw(3) << qty[i] << "\t\t" << right << setw(8) << price[i] << " \t\t" << right << setw(9) << tprice[i] << endl;
        }
        outfile.close();
    }
}

class ShowBill : public Bill
{
public:
    void output2();
};
void ShowBill::output2()
{
    input();
    output1();
    float cash = 0, net = 0, Qty = 0, amt = 0, cgst, sgst;
    int fnet;
    for (int i = 0; i < totalItems; i++)
    {
        amt += tprice[i];
        Qty += qty[i];
    }

    // GST Calculation
    cgst = 0.09 * amt;
    sgst = 0.09 * amt;
    net = amt + cgst + sgst;
    fnet = round(net);

    ofstream outfile("Bill_Book.TXT", ios::app);
    outfile << "\n------------------------------------------------------------------------------\n";
    outfile << "  Items: " << setw(4) << totalItems << "\t\tQty: " << setw(5) << Qty << "\t\t\tAmt: " << setw(12) << amt << endl;
    outfile << "\n------------------------------------------------------------------------------\n";

    cout << "\n------------------------------------------------------------------------------\n";
    cout << "  Items: " << setw(4) << totalItems << "\t\tQty: " << setw(5) << Qty << "\t\t\tAmt: " << setw(12) << amt << endl;
    cout << "\n------------------------------------------------------------------------------\n";

    // GST & NET Amount
    outfile << "  GST Break-Down\t\t  CGST: 9%\t\t  SGST: 9%\n";
    outfile << "------------------------------------------------------------------------------\n";
    outfile << "\t\t\t\t\tCGST: 9%\t: " << right << setw(15) << cgst << "\n\t\t\t\t\tSGST: 9%\t: " << right << setw(15) << sgst << endl;
    outfile << "\t\t\t\t\tTotal Amt\t: " << right << setw(15) << net << endl;
    outfile << "------------------------------------------------------------------------------\n";
    outfile << "\t\t\t\t\tNet Amount\t:" << right << setw(16) << fnet;
    outfile << "\n==============================================================================\n";

    cout << "  GST Break-Down\t\t  CGST: 9%\t\t  SGST: 9%\n";
    cout << "------------------------------------------------------------------------------\n";
    cout << "\t\t\t\t\tCGST: 9%\t: " << right << setw(15) << cgst << "\n\t\t\t\t\tSGST: 9%\t: " << right << setw(15) << sgst << endl;
    cout << "\t\t\t\t\tTotal Amt\t: " << right << setw(15) << net << endl;
    cout << "------------------------------------------------------------------------------\n";
    cout << "\t\t\t\t\tNet Amount\t:" << right << setw(16) << fnet;
    cout << "\n==============================================================================\n";

pay:
    int pm;
    cout << "\n\n\t\t\t * * * * PAYMENT SUMMARY * * * * \n";
    cout << "\n\t\t\t\t Payment Method:";
    cout << "\n\t\t\t 1.\t Cash";
    cout << "\n\t\t\t 2.\t UPI";
    cout << "\n\t\t\t 3.\t Card";
    cout << "\n\n\t\t\t Enter Payment Method: ";
    cin >> pm;
    switch (pm)
    {
    case 1:
        outfile << "\n\t\t\t Recived Rs." << fnet << "\n\t\t\t Payment Mode: cash.\n";
        cout << "\n\n\t\t\t   Recive Rs." << fnet << " in cash.\n";
        system("PAUSE");
        cout << "\t\t\t     Recived In Cash!\n\t\t\t        Thank You!\n";
        cout << "\n\n\t\t\tYou Are Still Logged In!\n";
        break;
    case 2:
        outfile << "\n\t\t\t   Recive Rs." << fnet << "\n\t\t\t Payment Mode: UPI.\n";
        cout << "\n\n\t\t\t   Recive Rs." << fnet << " in UPI.\n";
        system("PAUSE");
        cout << "\t\t\t     Recived In UPI!\n\t\t\t        Thank You!\n";
        cout << "\n\n\t\t\tYou Are Still Logged In!\n";
        break;
    case 3:
        outfile << "\n\t\t\t   Recive Rs." << fnet << "\n\t\t\t Payment Mode: card.\n";
        cout << "\n\n\t\t\t   Recive Rs." << fnet << " in card.\n";
        system("PAUSE");
        cout << "\t\t\t     Recived In Card!\n\t\t\t        Thank You!\n";
        cout << "\n\n\t\t\tYou Are Still Logged In!\n";
        break;
    default:
        cout << "\a";
    }
    outfile.close();
}

// Admin class
class Admin : virtual public Bill
{
protected:
    string apw;
    string nuser, pwuser, staffN;

public:
    void header()
    {
        LoginManager signup;
        if (access() == 0)
        {
            int c;
        head:
            do
            {
                system("CLS");
                cout << "\n\n\t\t\t------------------------------";
                cout << "\n\t\t\t\t ADMIN CONSOLE";
                cout << "\n\t\t\t------------------------------";
                cout << "\n\t\t\t1.\tAdd staff.\n\t\t\t2.\tReturn Console." << endl;
                cout << "\n\n\t\t\tEnter your option: ";
                cin >> c;
                switch (c)
                {
                case 1:
                {
                    system("CLS");
                    cout << "\n\t\t\t\t Sign-up New staff:" << endl;
                    cout << "\n\t\t\t Enter staff name: ";
                    cin >> staffN;
                    cout << "\n\t\t\t Enter staff user name: ";
                    cin >> nuser;
                    cout << "\n\t\t\t Enter staff Password: ";
                    cin >> pwuser;
                    signup.addUser(staffN, nuser, pwuser);
                    cout << "\n\t\tNew Staff User Name & Password Stored In The System!" << endl;
                    system("PAUSE");
                    goto head;
                }
                case 2:
                    return;
                default:
                    cout << "\a";
                }

            } while (c != 2);
        }
    }
    int access()
    {
        cout << "\n\n\n\t\t\tEnter Access Password: ";
        cin >> apw;
        if (apw == "ABHI")
        {
            return 0;
        }
        else
        {
            cout << "\n\n\n\t\t\tPlease enter correct Access Password!!!" << endl;
        }
    }
};

// Main

int main()
{
    system("PAUSE");
    system("CLS");

    // Login
    LoginManager log;
    // log.addUser("Kamal", "kpm", "kpm1"); // this for Initial user login

    cout << "\n\n\t\t\t------------------------------";
    cout << "\n\t\t\t\t***WELCOME***";
    cout << "\n\t\t\t------------------------------\n";
    log.login();

    // Main Console
    ShowBill obj;
    Admin h;

    char ch;
    int opt;
    int a = 1;
    ifstream fin;
main:
    do
    {
    start:
        system("PAUSE");
        system("CLS");
        cout << "\n\n\t\t\t------------------------------";
        cout << "\n\t\t\t  Billing Management System";
        cout << "\n\t\t\t------------------------------";
        cout << "\n\n\t\t\tWhat you want to do?";
        cout << "\n\t\t\t1.\tGenerate Bill\n\t\t\t2.\tView Previous Bills\n\t\t\t3.\tAccess Admin Console\n\t\t\t4.\tExit\n";
        cout << "\n\n\t\t\tEnter your option: ";
        cin >> opt;
        switch (opt)
        {
        case 1:
            obj.output2();
            goto start;
        case 2:
            fin.open("Bill_Book.TXT", ios::in);
            while (fin.get(ch))
            {
                cout << ch;
            }
            fin.close();

            goto start;
        case 3:
            h.header();
            goto start;

        case 4:
            exit(0);
        default:
            cout << "\a";
        }

    } while (opt != 4);

    getch();
}