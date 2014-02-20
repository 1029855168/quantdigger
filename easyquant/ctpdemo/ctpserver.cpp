#include "ctpserver.h"
#include <iostream>

extern TThostFtdcBrokerIDType appId;		// Ӧ�õ�Ԫ
extern TThostFtdcUserIDType userId;		// Ͷ���ߴ���


extern int requestId; 

// �Ự����
extern int	 frontId;	//ǰ�ñ��
extern int	 sessionId;	//�Ự���
extern char orderRef[13];

namespace EasyQuant {
using namespace std;
CtpServer::CtpServer(char *tradeFront) {
        user_ = CThostFtdcMdApi::CreateFtdcMdApi();
        user_->RegisterSpi(dynamic_cast<CThostFtdcMdSpi*>(this));			// ע���¼���
        RegisterFront(tradeFront);							// ע�ύ��ǰ�õ�ַ
};




void CtpServer::OnHeartBeatWarning(int nTimeLapse) {
}

void CtpServer::ReqUserLogin(TThostFtdcBrokerIDType	vAppId,
                             TThostFtdcUserIDType	vUserId,	
                             TThostFtdcPasswordType	vPasswd) {
    CThostFtdcReqUserLoginField req;
    memset(&req, 0, sizeof(req));
    strcpy(req.BrokerID, vAppId); strcpy(appId, vAppId); 
    strcpy(req.UserID, vUserId);  strcpy(userId, vUserId); 
    strcpy(req.Password, vPasswd);
    int ret = user_->ReqUserLogin(&req, ++requestId);
    cerr<<" sending | ���͵�¼..."<<((ret == 0) ? "�ɹ�" :"ʧ��") << endl;	
}

void CtpServer::OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin, 
                               CThostFtdcRspInfoField *pRspInfo, 
                               int nRequestID, 
                               bool bIsLast) {
	if ( !IsErrorRspInfo(pRspInfo) && pRspUserLogin ) {  
    // ����Ự����	
		frontId = pRspUserLogin->FrontID;
		sessionId = pRspUserLogin->SessionID;
		int nextOrderRef = atoi(pRspUserLogin->MaxOrderRef);
		sprintf(orderRef, "%d", ++nextOrderRef);
       cerr<<" ��Ӧ | ��¼�ɹ�...��ǰ������:"
       <<pRspUserLogin->TradingDay<<endl;     
       // Ҫ���յĺ�Լ����
       char* d[]= { "ru1405" };
        SubscribeMarketData(d, 1);
  }
//  if(bIsLast) sem.sem_v();
}




void CtpServer::OnRspError(CThostFtdcRspInfoField *pRspInfo, 
                           int nRequestID, 
                           bool bIsLast) {
}




bool CtpServer::IsErrorRspInfo(CThostFtdcRspInfoField *pRspInfo) {
	// ���ErrorID != 0, ˵���յ��˴������Ӧ
	bool ret = ((pRspInfo) && (pRspInfo->ErrorID != 0));
  if (ret){
    cerr<<" ��Ӧ | "<<pRspInfo->ErrorMsg<<endl;
  }
	return ret;
}


int CtpServer::ReqUserLogout(CThostFtdcUserLogoutField *pUserLogout, int nRequestID) {
}

void CtpServer::OnRspUserLogout(CThostFtdcUserLogoutField *pUserLogout, 
                                CThostFtdcRspInfoField *pRspInfo, 
                                int nRequestID, 
                                bool bIsLast) {
}

int CtpServer::UnSubscribeMarketData(char *ppInstrumentID[], int nCount) {
}

void CtpServer::OnRspUnSubMarketData(CThostFtdcSpecificInstrumentField *pSpecificInstrument,
                                     CThostFtdcRspInfoField *pRspInfo,
                                     int nRequestID,bool bIsLast) {
}


int CtpServer::SubscribeMarketData(char *ppInstrumentID[], int nCount) {
    if(0 == user_->SubscribeMarketData(ppInstrumentID, nCount))
        cout<<"SubscribeMarketData sucess"<<endl;
    else
        cout<<"SubscribeMarketData error"<<endl;
}

void CtpServer::OnRspSubMarketData(CThostFtdcSpecificInstrumentField *pSpecificInstrument, 
                                   CThostFtdcRspInfoField *pRspInfo, 
                                   int nRequestID, 
                                   bool bIsLast) {
    if (!IsErrorRspInfo(pRspInfo)) {
        cerr<<"��Ӧ | �������ݣ�"<<endl;
    } else {
        cerr<<"************"<<endl;
    }
}


void CtpServer::RegisterNameServer(char *pszNsAddress) {
}


void CtpServer::RegisterFront(char *pszFrontAddress) {
    user_->RegisterFront(pszFrontAddress);
    cerr<<"���ӽ���ǰ��..."<<endl;
}

void CtpServer::OnFrontConnected() {
	cerr<<" ���ӽ���ǰ��...�ɹ�"<<endl;
    ReqUserLogin("1035", "00000071", "123456");
}

void CtpServer::OnFrontDisconnected(int nReason) {
	cerr<<" ��Ӧ | �����ж�..." 
	  << " reason=" << nReason << endl;
}

void CtpServer::OnRtnDepthMarketData(CThostFtdcDepthMarketDataField *pDepthMarketData) {
    cerr<<pDepthMarketData->LastPrice<<endl;
}

} /* EasyQuant */
