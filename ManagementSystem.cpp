#include <iostream>
#include <string>
#include <conio.h>
using namespace std;

class admin //운영자 
{
private:
	string const username = "문영현"; //운영자 계정 아이디
	string const password = "0000"; //운영자 계정 비밀번호
public:
	admin() { }
	string getUsername() const { return username; }
	string getPassword() const { return password; }
};
class item //제품
{
private:
	string name; //제품 이름
	string description; //제품 설명
public:
	item(string n = "", string d = "") { name = n; description = d; }
	void setItemName(string type) {
		cout << " 제품 이름 입력: " << type;
		cin >> name; //제품 이름 입력
	}
	void setItemDescription(string type) {
		cout << " 제품 설명 입력: " << type;
		cin >> description; // 제품 설명 입력
	}
	string getItemName() const { return name; }
	string getItemDescription() const { return description; }
	void removeItem() { name = ""; description = ""; } //제품제거 함수
};

class deal : public item //거래 <- 제품 (상속)
{
private:
	string dealName; //주문명
	int dealItems; //주문물품
	string coldDrink; //음료
	string fries; // 튀김
	double dealPrice; //주문가격

public:
	deal(string dn = " ", int di = 0, string in = " ", string id = " ", string cd = " ", string f = " ", double dp = 0.00) :item(in, id) {
		dealName = dn;
		dealItems = di;
		coldDrink = cd;
		fries = f;
		dealPrice = dp;
	}

	void removeDeal() {
		dealName = " ";
		dealItems = 0;
		coldDrink = " ";
		fries = " ";
		dealPrice = 0.00;
		removeItem();
	} //주문취소

	void showDeal() const {
		cout << "--------" << dealName << "--------";
		cout << " 수량: " << dealItems << "--------";
		cout << " 설명: " << " " << item::getItemDescription();
		cout << " 음료: " << coldDrink;
		cout << " 튀김: " << fries;
		cout << " 결제 가격: " << dealPrice;
	}

	void setDealName() {
		cout << " 메뉴명: ";
		cin >> dealName;
	} //메뉴명

	void setDealItems() {
		cout << " 메뉴 수량: ";
		cin >> dealItems;
	}//

	void setColdDrink() {
		cout << " 음료: ";
		cin >> coldDrink;
	} // 음료주문

	void setFries() {
		cout << " 튀김: ";
		cin >> fries;
	} //튀김주문

	void setDealPrice() {
		cout << " 결제가격: ";
		cin >> dealPrice;
	}//주문가격

	string getDealName() const { return dealName; } //주문명 리턴
	int getDealItems() const { return dealItems; } //주문수단 리턴
	string getColdDrink() const { return coldDrink; } //음료 리턴
	string getFries() const { return fries; } //튀김 리턴
	double getDealPrice() const { return dealPrice; } //주문가격 리턴
};

class address//주소
{
private:
	string societyName;
	int streetNumber;
	int houseNumber;
public:
	address(string sn = "", int strn = 0, int hn = 0) {
		societyName = sn;
		streetNumber = strn;
		houseNumber = hn;
	}
	void setSocietyName() {
		cout << " 건물이름을 입력하세요 ";
		cin >> societyName; //소셔티 이름 입력
	}
	void setStreetNumber() {
		cout << " 거리번호를 입력하세요";
		cin >> streetNumber; //거리번호 입력
	}
	void setHouseNumber() {
		cout << " 집번호를 입력하세요: ";
		cin >> houseNumber; //집번호 입력
	}
	string getScocietyName() const { return societyName; } //소셔티 이름 리턴
	int getStreetNumber() const { return streetNumber; } //거리번호 리턴
	int getHouseNumber() const { return houseNumber; } // 집번호 리턴
};

class userDetails //시스템 유저
{
private:
	string name; //유저 명
	address addressOfCustomer; //유저의 주소
	long phoneNumber; //유저 핸드폰 번호
public:
	userDetails(string n = "", string society = " ", int streetNum = 0, int houseNum = 0, long pn = 0) :addressOfCustomer(society, streetNum, houseNum) {
		name = n;
		phoneNumber = pn;
	}
	void setName() {
		cout << "이름을 입력하세요 ";
		cin >> name;
	}
	void setAddress() {
		addressOfCustomer.setSocietyName();
		addressOfCustomer.setStreetNumber();
		addressOfCustomer.setHouseNumber();
	}
	void setPhoneNumber() {
		cout << "핸드폰 번호를 입력하세요";
		cin >> phoneNumber;
	}
	string getName() const { return name; }
	string getSocietyName() const { return addressOfCustomer.getScocietyName(); }
	int getStreetNumber() const { return addressOfCustomer.getStreetNumber(); }
	int getHouseNumber() const { return addressOfCustomer.getHouseNumber(); }
	long getPhoneNumber() const { return phoneNumber; }
};

class date //날짜 
{
private:
	int day; //일
	int month; //월
	int year; //년도

public:
	date(int d = 0, int m = 0, int y = 0) {
		day = d;
		month = m;
		year = y;
	}
	void setDay(int d) { day = d; }
	void setMonth(int m) { month = m; }
	void setYear(int y) { year = y; }
	int getDay() const { return day; } // 일 리턴
	int getMonth() const { return month; } //월 리턴
	int getYear() const { return year; } //년도 리턴
};

class orderDetails //주문사항 클래스
{
private:
	int orderID; //주문ID
	string dealName; //주문명
	userDetails customerDetails; //주문사항
	date orderDate; //주문날짜
	string orderStatus; //주문상태
public:
	orderDetails(int oID = 0, string dealN = "", double oP = 0.00, string oS = "") {
		orderID = oID;
		dealName = dealN;
		orderStatus = oS;
	}
	void display() const {
		cout << " -------- 주문#" << orderID << " --------" << endl;
		cout << " 거래명: " << dealName << endl;
		cout << " 주문 상태: " << orderStatus << endl;
		cout << " 고객 이름: " << customerDetails.getName() << endl;
		cout << " 고객 번호: " << customerDetails.getPhoneNumber() << endl;
		cout << " 주문한 날짜: " << orderDate.getDay() << "/" << orderDate.getMonth() << "/" << orderDate.getYear() << " " << endl;
	}
	void setOrderID() { orderID++; }
	void setDealNumber(string dn) { dealName = dn; }
	void setOrderStatus(string oS) { orderStatus = oS; }
	void setCustomerDetails() {
		customerDetails.setName();
		customerDetails.setPhoneNumber();
		customerDetails.setAddress();
	}
	void setOrderDate(int d, int m, int y) {
		orderDate.setDay(d);
		orderDate.setMonth(m);
		orderDate.setYear(y);
	}
	int getOrderID() const { return orderID; }
	string getDealName() const { return dealName; }
	string getOrderStatus() const { return orderStatus; }
};

class fastFoodRestaurant //식당
{
private:
	string restaurantName; //식당이름
	admin administrator; //식당운영자
	deal deals[5];
	int dealSlot = 0;
	orderDetails orders[20];
	int activeOrders;
	date currentDate;
public:
	fastFoodRestaurant(string rn = "", int ao = 0) {
		restaurantName = rn;
		activeOrders = ao;
	}
	void setRestaurantName(string rn) { restaurantName = rn; }
	void setActiveOrders() { activeOrders++; }
	string getRestaurantName() const { return restaurantName; }
	int getActiveOrders() const { return activeOrders; }
	string getAdminUsername() const { return administrator.getUsername(); }
	string getAdminPassword() const { return administrator.getPassword(); }

	void setDeal() {
		int flag = 1;
		while (flag == 1) {
			int i = dealSlot;
			string itemType;

			for (i; i < 5; i++) {
				deals[i].setDealName();
				deals[i].setDealItems();

				cout << " 메뉴 종류를 입력하세요" << endl;
				cin >> itemType;

				deals[i].setItemName(itemType);
				deals[i].setItemDescription(itemType);
				deals[i].setColdDrink();
				deals[i].setFries();
				deals[i].setDealPrice();

				system("cls");
				cout << "- 거래 추가됨 -" << endl;
				cout << " 거래를 추가하려면 1을 누르고 메뉴를 종료하려면 0을 누르십시오" << endl;
				cin >> flag;

				if (flag == 0) {
					dealSlot = i + 1;
					break;
				}
			}
		}
	}
	void removeDeal() {
		string removeDealName;
		int flag = 0;

		cout << " 취소할 음식을 입력하세요: " << endl;
		cin >> removeDealName;

		for (int i = 0; i < 5; i++) {
			if (removeDealName == deals[i].getDealName()) {
				deals[i].removeDeal();
				flag = 1;
				cout << " 거래가 취소되었습니다" << endl;
				cout << " 엔터 키를 눌러 메뉴로 돌아가세요." << endl;
				_getwch();
			}
		}

		if (flag == 0) {
			cout << " 존재하지 않는 거래입니다." << endl;
			cout << " 엔터 키를 눌러 메뉴로 돌아가세요." << endl;
			_getwch();
		}
	}

	void viewOrders() const {
		for (int i = 0; i < 20; i++) {
			if (orders[i].getOrderID() != 0) {
				orders[i].display();
			}
		}
		cout << " 엔터 키를 눌러 메뉴로 돌아가세요" << endl;
		_getwch();
	}

	void changeOrderStatus() {
		for (int i = 0; i < 20; i++) {
			if (orders[i].getOrderID() != 0) {
				string orderStatus;
				cout << " 주문# " << orders[i].getOrderID() << endl;
				cout << " 주문상태(진행 중/취소/배달 중): ", cin >> orderStatus;
				orders[i].setOrderStatus(orderStatus);
			}
		}
		cout << " 엔터 키를 눌러 메뉴로 돌아가세요" << endl;
		_getwch();
	}
	void displayMenu() const {
		for (int i = 0; i < 5; i++) {
			if (deals[i].getDealName() != " ") { deals[i].showDeal(); }
		}
		cout << " 엔터 키를 눌러 메뉴로 돌아가세요" << endl;
		_getwch();
	}
	void setOrder(int& orderSlot) {
		string dealName;

		orders[orderSlot].setCustomerDetails();
		cout << " 주문명을 입력하세요 ";
		cin >> dealName;
		orders[orderSlot].setDealNumber(dealName);
		orders[orderSlot].setOrderDate(currentDate.getDay(), currentDate.getMonth(), currentDate.getYear());
		orders[orderSlot].setOrderID();

		cout << " 엔터 키를 눌러 메뉴로 돌아가세요" << endl;
		_getwch();
	}
	void setDate() {
		int day, month, year;
		cin >> year;  cin >> month;  cin >> day;

		currentDate.setYear(year);
		currentDate.setMonth(month);
		currentDate.setDay(day);
	}

	void viewOrderForCurrentCustomer(int orderSlot) const {
		orders[orderSlot].display();

		cout << "엔터 키를 눌러 메뉴로 돌아가세요." << endl;
		_getwch();
	}

	void viewOrderStatusForCurrentCustomer(int orderSlot) const {
		cout << " 주문상태: " << orders[orderSlot].getOrderStatus() << endl;

		cout << "엔터 키를 눌러 메뉴로 돌아가세요." << endl;
		_getwch();
	}
};

void startmenu(fastFoodRestaurant ls, int os); //시작페이지
void mainMenu(fastFoodRestaurant ls, int os); //메인페이지
//void adminLogin(fastFoodRestaurant ls, int os); //운영자 로그인 페이지
void adminMenu(fastFoodRestaurant ls, int os); //운영자 페이지
//void userMenu(fastFoodRestaurant ls, int os); //사용자 페이지

void startmenu(fastFoodRestaurant ls, int os) {
	int orderSlot = 0;
	int userOption = 0;
	int loginOption = 0;

	cout << "프로그램을 실행하기 전, 접속 날짜를 입력하세요 " << endl;
	ls.setDate();

	system("cls");

	cout << " ===============================" << endl;
	cout << " |                             |" << endl;
	cout << " |                             |" << endl;
	cout << " |         조선 식당에         |" << endl;
	cout << " |   어서오세요  환영합니다.   |" << endl;
	cout << " |                             |" << endl;
	cout << " |                             |" << endl;
	cout << " ===============================" << endl;
	cout << " 아무거나 입력하여 진행하세요..." << endl;
	_getch();

	system("cls");
}

void mainMenu(fastFoodRestaurant ls, int os) {
	int loginOption = 0;
	int userOption = 0;
	int orderSlot = os;

	cout << " ===============================" << endl;
	cout << " |                             |" << endl;
	cout << " |      옵션을 선택하세요      |" << endl;
	cout << " |         1) 관리자           |" << endl;
	cout << " |         2) 사용자           |" << endl;
	cout << " |         3) 종료             |" << endl;
	cout << " |                             |" << endl;
	cout << " ===============================" << endl;
	cin >> loginOption;
	system("cls");

	string username, password;

	while (1) {
		if (loginOption == 1)
		cout << " ===============================" << endl;
		cout << "                              " << endl;
		cout << "         - 로그인 -           " << endl;
		cout << "        사용자이름: ", cin >> username;
		cout << "        패스워드: ", cin >> password;
		cout << "                              " << endl;
		cout << "                              " << endl;
		cout << " ===============================" << endl;

		if ((ls.getAdminPassword() == password) && (ls.getAdminUsername() == username)) {
			system("cls");
			int adminOption = 0;
			cout << " ===============================" << endl;
			cout << " |                             |" << endl;
			cout << " |   원하는 옵션을 선택하세요  |" << endl;
			cout << " |      1) 거래 추가           |" << endl;
			cout << " |      2) 거래 취소           |" << endl;
			cout << " |      3) 주문 조회           |" << endl;
			cout << " |      4) 주문 상태 변경      |" << endl;
			cout << " |      5) 메뉴 조회           |" << endl;
			cout << " |      6) 로그아웃            |" << endl;
			cout << " |                             |" << endl;
			cout << " ===============================" << endl;
			cin >> adminOption;
			system("cls");

			switch (adminOption)
			{
			case 1:
				ls.setDeal();
				system("cls");
				adminMenu(ls, os);
				break;
			case 2:
				ls.removeDeal();
				system("cls");
				adminMenu(ls, os);
				break;
			case 3:
				ls.viewOrders();
				system("cls");
				adminMenu(ls, os);
				break;
			case 4:
				ls.changeOrderStatus();
				system("cls");
				adminMenu(ls, os);
				break;
			case 5:
				ls.displayMenu();
				system("cls");
				adminMenu(ls, os);
				break;
			case 6:
				mainMenu(ls, os);
				break;
			default:
				cout << " Wrong option entered, enter option again!" << endl;
				adminMenu(ls, os);
				break;
			}
		}
		else {
			cout << "잘못된 정보가 입력됬습니다! 다시 입력하세요" << endl;
			_getwch();
			system("cls");
		}

	if (loginOption == 3) {
			cout << " ===============================" << endl;
			cout << " |                             |" << endl;
			cout << " |                             |" << endl;
			cout << " |      조선 식당을 이용       |" << endl;
			cout << " |     해주셔서 감사합니다     |" << endl;
			cout << " |                             |" << endl;
			cout << " |                             |" << endl;
			cout << " ===============================" << endl;
			break;
	}

		/*
	case 2:
		cout << " ===============================" << endl;
		cout << " |                             |" << endl;
		cout << " |  원하는 옵션을 선택하세요.  |" << endl;
		cout << " |      1) 메뉴 보기           |" << endl;
		cout << " |      2) 주문                |" << endl;
		cout << " |      3) 주문 조회           |" << endl;
		cout << " |      4) 주문 상태 조회      |" << endl;
		cout << " |      5) 종료                |" << endl;
		cout << " |                             |" << endl;
		cout << " ===============================" << endl;
		cin >> userOption;
		system("cls");

		switch (userOption) {
		case 1:
			lS.displayMenu();
			system("cls");
			//userMenu(lS, oS);
			break;
		case 2:
			if (orderSlot < 20) { lS.setOrder(orderSlot); }
			else if (orderSlot >= 20) {
				cout << " 나중에 다시 주문하십시오. 불편을 끼쳐드려 죄송합니다. " << endl;
			}
			system("cls");
			//userMenu(lS, oS);
			break;
		case 3:
			lS.viewOrderForCurrentCustomer(orderSlot);
			system("cls");
			//userMenu(lS, oS);
			break;
		case 4:
			lS.viewOrderStatusForCurrentCustomer(orderSlot);
			system("cls");
			//userMenu(lS, oS);
			break;
		case 5:
			mainMenu(lS, orderSlot);
			break;
		default:
			cout << "잘못된 옵션입니다. 다시 입력하세요!" << endl;
			_getwch();
			system("cls");
			//userMenu(lS, oS);
		}
		break;*/
	}
}

int main(){
	fastFoodRestaurant ls;
	int os = 0;
	startmenu(ls, os); //시작메세지
	mainMenu(ls, os); //메인페이지
}

/*--------------------------------------------------------------------------------------------------------------------------*/
/*
void adminLogin(fastFoodRestaurant ls, int os){ //운영자 로그인 창 출력 함수
	string username, password;

	cout << " ===============================" << endl;
	cout << "                              " << endl;
	cout << "         - 로그인 -           " << endl;
	cout << "        사용자이름: ", cin >> username;
	cout << "        패스워드: ", cin >> password;
	cout << "                              " << endl;
	cout << "                              " << endl;
	cout << " ===============================" << endl;

	if ((ls.getAdminPassword() == password) && (ls.getAdminUsername() == username)){ //입력이 운영자의 정보와 일치할 경우에 실행
		system("cls");
		int adminOption = 0;
		cout << " ===============================" << endl;
		cout << " |                             |" << endl;
		cout << " |  원하는 옵션을 선택하세요   |" << endl;
		cout << " |      1) 거래 추가           |" << endl;
		cout << " |      2) 거래 취소           |" << endl;
		cout << " |      3) 주문 조회           |" << endl;
		cout << " |      4) 주문 상태 변경      |" << endl;
		cout << " |      5) 메뉴 조회           |" << endl;
		cout << " |      6) 로그 아웃           |" << endl;
		cout << " |                             |" << endl;
		cout << " ===============================" << endl;
		cin >> adminOption;
		system("cls");
		switch (adminOption)
		{
		case 1:
			ls.setDeal();
			system("cls");
			adminMenu(ls, os);
			break;
		case 2:
			ls.removeDeal();
			system("cls");
			adminMenu(ls, os);
			break;
		case 3:
			ls.viewOrders();
			system("cls");
			adminMenu(ls, os);
			break;
		case 4:
			ls.changeOrderStatus();
			system("cls");
			adminMenu(ls, os);
			break;
		case 5:
			ls.displayMenu();
			system("cls");
			adminMenu(ls, os);
			break;
		case 6:
			mainMenu(ls, os);
			break;
		default:
			cout << "잘못된 옵션입니다. 다시 입력하세요!" << endl;
			adminMenu(ls, os);
			break;
		}
	}
	else{ //입력한 운영자 정보가 잘못된 경우
		cout << "잘못된 정보가 입력됬습니다! 다시 입력하세요" << endl;
		_getwch();
		system("cls");
		adminLogin(ls, os);
	}
}*/

void adminMenu(fastFoodRestaurant ls, int os){ //운영자로 접속시 출력되는 함수
		int adminOption = 0;
		cout << " ===============================" << endl;
		cout << " |                             |" << endl;
		cout << " |   원하는 옵션을 선택하세요  |" << endl;
		cout << " |      1) 거래 추가           |" << endl;
		cout << " |      2) 거래 취소           |" << endl;
		cout << " |      3) 주문 조회           |" << endl;
		cout << " |      4) 주문 상태 변경      |" << endl;
		cout << " |      5) 메뉴 조회           |" << endl;
		cout << " |      6) 로그아웃            |" << endl;
		cout << " |                             |" << endl;
		cout << " ===============================" << endl;
		cin >> adminOption;
		system("cls");

		switch (adminOption)
		{
		case 1:
			ls.setDeal();
			system("cls");
			adminMenu(ls, os);
			break;
		case 2:
			ls.removeDeal();
			system("cls");
			adminMenu(ls, os);
			break;
		case 3:
			ls.viewOrders();
			system("cls");
			adminMenu(ls, os);
			break;
		case 4:
			ls.changeOrderStatus();
			system("cls");
			adminMenu(ls, os);
			break;
		case 5:
			ls.displayMenu();
			system("cls");
			adminMenu(ls, os);
			break;
		case 6:
			mainMenu(ls, os);
			break;
		default:
			cout << "잘못된 정보가 입력됬습니다! 다시 입력하세요" << endl;
			adminMenu(ls, os);
			break;
		}
}
/*
void userMenu(fastFoodRestaurant ls, int os){ //사용자 메뉴 출력
	int userOption = 0; //사용자 선택 옵션 1~5

	cout << " ===============================" << endl;
	cout << " |                             |" << endl;
	cout << " |  원하는 옵션을 선택하세요.  |" << endl;
	cout << " |      1) 메뉴 보기           |" << endl;
	cout << " |      2) 주문                |" << endl;
	cout << " |      3) 주문 조회           |" << endl;
	cout << " |      4) 주문 상태 조회      |" << endl;
	cout << " |      5) 종료                |" << endl;
	cout << " |                             |" << endl;
	cout << " ===============================" << endl;
	cin >> userOption; //옵션 입력
	system("cls");

	switch (userOption){
	case 1:
		ls.displayMenu();
		system("cls");
		userMenu(ls, os);
		break;
	case 2:
		if (os < 20){ls.setOrder(os);}
		else if (os >= 20){
			cout << " 나중에 다시 주문하십시오. 불편을 끼쳐드려 죄송합니다. " << endl;
		} // 주문량이 20이상일 경우 출력되는 안내 메세지
		system("cls");
		userMenu(ls, os);
		break;
	case 3:
		ls.viewOrderForCurrentCustomer(os);
		system("cls");
		userMenu(ls, os);
		break;
	case 4:
		ls.viewOrderStatusForCurrentCustomer(os);
		system("cls");
		userMenu(ls, os);
		break;
	case 5:w
		mainMenu(ls, os);
		break;
	default:
		system("cls");
		userMenu(ls, os);
	}
} */
