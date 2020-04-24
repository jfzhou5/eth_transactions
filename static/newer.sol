pragma solidity ^0.5.1;
contract securityTransction{

    struct IPO{
        address payable ipo_addr;
        uint stock_id;
        uint ipo_count;
        uint ipo_price;
        uint stock_price;
    }

    struct stocker{
        address payable stocker_addr;
        mapping (uint => uint) stocks;
    }

    struct trans_info{
        address payable trans_addr;
        uint stock_id;
        uint stock_count;
        uint stock_price;
    }

    mapping (uint => IPO) public IPOS;
    uint public ipo_index = 0;

    mapping (uint => stocker) public stockers;
    uint public stockers_index = 0;

    mapping (uint =>trans_info) public buys;
    uint public buys_index = 0;

    mapping (uint =>trans_info) public sells;
    uint public sells_index = 0;

    uint [] stock_ids;

    function get_stock_ids() public view returns(uint [] memory){
        return stock_ids;
    }

    function add_ipo(uint stock_id,uint ipo_count,uint ipo_price) public payable returns (address){
        IPOS[stock_id] = IPO(msg.sender,stock_id,ipo_count,ipo_price,ipo_price);
        stock_ids.push(stock_id);
        ipo_index = ipo_index+1;
        return msg.sender;
    }
    // stockHolder add stock
    function addStock(address Addr,uint stock_id,uint stock_count) payable public{
        for(uint i=0;i<stockers_index;i++){
            if(stockers[i].stocker_addr == Addr){
                stockers[i].stocks[stock_id] = stockers[i].stocks[stock_id]+stock_count;
                return ;
            }
        }
        address payable s_addr = address(uint160(Addr)); // 正确，先转换为uint160，然后转换为address payable
        stockers[stockers_index].stocker_addr =  s_addr;
        stockers[stockers_index].stocks[stock_id] = stock_count;
        stockers_index = stockers_index+1;
    }

    function subStock(address Addr,uint stock_id,uint stock_count) public{
        for(uint i=0;i<stockers_index;i++){
            if(stockers[i].stocker_addr == Addr){
                stockers[i].stocks[stock_id] = stockers[i].stocks[stock_id]-stock_count;
            }
        }
    }


    function clear() public payable returns(bool){
        for (uint i=0;i<buys_index;i++){
            for (uint j=0;j<sells_index;j++){
                if (buys[i].stock_id == sells[j].stock_id && buys[i].stock_price == sells[j].stock_price){
                    if (buys[i].stock_count > sells[j].stock_count){

                        sells[j].trans_addr.transfer(sells[j].stock_count * sells[j].stock_price*10**18);

                        subStock(sells[j].trans_addr,sells[j].stock_id,sells[j].stock_count);
                        buys[i].stock_count = buys[i].stock_count - sells[j].stock_count;
                        addStock(buys[i].trans_addr,buys[i].stock_id,sells[j].stock_count);
                        delete sells[j];



                    }else if(buys[i].stock_count < sells[j].stock_count){
                        sells[j].trans_addr.transfer(buys[i].stock_count * sells[j].stock_price *10**18);
                        subStock(sells[j].trans_addr,sells[j].stock_id,buys[i].stock_count);
                        sells[j].stock_count = sells[j].stock_count - buys[i].stock_count;
                        addStock(buys[i].trans_addr,buys[i].stock_id,buys[i].stock_count);
                        delete buys[i];


                    }else if(buys[i].stock_count == sells[j].stock_count){
                        sells[j].trans_addr.transfer(buys[i].stock_count * sells[j].stock_price*10**18);
                        subStock(sells[j].trans_addr,sells[j].stock_id,buys[i].stock_count);
                        addStock(buys[i].trans_addr,buys[i].stock_id,buys[i].stock_count);
                        delete buys[i];
                        delete sells[j];

                    }
                }
            }
        }
        for (uint i=0;i<buys_index;i++){
            if (buys[i].stock_price == IPOS[buys[i].stock_id].ipo_price){
                if (buys[i].stock_count<=IPOS[buys[i].stock_id].ipo_count){
                    IPOS[buys[i].stock_id].ipo_count -= buys[i].stock_count;
                    IPOS[buys[i].stock_id].ipo_addr.transfer(buys[i].stock_count*buys[i].stock_price*10**18);
                    addStock(buys[i].trans_addr,buys[i].stock_id,buys[i].stock_count);
                    delete buys[i];

                }
            }
        }

    }

    function buy(uint stock_id,uint stock_count,uint stock_price) public payable returns (bool){
        buys[buys_index] = trans_info(msg.sender,stock_id,stock_count,stock_price);
        buys_index = buys_index +1;
        if (clear()) return true;
        else return false;
    }

    function sell(uint stock_id,uint stock_count,uint stock_price) public payable returns (bool){
        sells[sells_index] = trans_info(msg.sender,stock_id,stock_count,stock_price);
        sells_index = sells_index +1;
        if (clear()) return true;
        else return false;
    }

    function getSenderBalance(address addr) public view returns (uint){
        return addr.balance;
    }

    function getConBalance() public view returns(uint){
        return address(this).balance;
    }

    function get_stock_price(uint stock_id) public view returns(uint){
        uint price = 0;
        if (IPOS[stock_id].ipo_count==0) price = 0;
        else price = IPOS[stock_id].ipo_price;
        for(uint i=0;i<buys_index;i++){
            if (buys[i].stock_price!=0 && price>=buys[i].stock_price && buys[i].stock_id == stock_id ){
                price = buys[i].stock_price;
            }
        }
        return price;
    }


    function get_buys(uint index) public view returns (address trans_addr,uint stock_id,uint stock_count,uint stock_price){
        trans_addr = buys[index].trans_addr;
        stock_id = buys[index].stock_id;
        stock_count = buys[index].stock_count;
        stock_price = buys[index].stock_price;
    }

    function get_sells(uint index) public view returns (address trans_addr,uint stock_id,uint stock_count,uint stock_price){
        trans_addr = sells[index].trans_addr;
        stock_id = sells[index].stock_id;
        stock_count = sells[index].stock_count;
        stock_price = sells[index].stock_price;
    }

    function get_buys_index() public view returns (uint){
        return buys_index;
    }

    function get_sells_index() public view returns (uint){
        return sells_index;
    }

    uint [] ids;
    uint [] counts;
    function get_stockers_all_stocks(address addr) public payable returns(uint [] memory,uint [] memory){

        // uint [] memory ids = new uint[](1);
        // uint [] memory counts = new uint[](1);
        ids.length=0;
        counts.length=0;
        uint x = 0;
        for (uint j=0;j<stockers_index;j++){
            if (stockers[j].stocker_addr == addr){

                for (uint i=0;i<ipo_index;i++){
                    if(stockers[j].stocks[stock_ids[i]]!=0){

                        ids.push(stock_ids[i]);
                        counts.push(stockers[j].stocks[stock_ids[i]]);
                        x++;

                    }
                }
            }
        }
        return (ids,counts);
    }

    function get_id_counts() public view returns(uint [] memory,uint [] memory){
        return (ids,counts);
    }

    function get_stockers_index() public view returns(uint){
        return stockers_index;
    }


    function get_ipo_from_id(uint id) public view returns(uint count,uint ipo_price,uint new_price){
        count = IPOS[id].ipo_count;
        ipo_price = IPOS[id].ipo_price;
        new_price = get_stock_price(id);
    }



}