pragma solidity ^0.4.2;

contract SplitSell {
    event onBuy();

    struct Share {
        uint32 buyValue;
        address owner;
        bytes32 ownerName;
        bytes32 ownerRRN;
    }
    struct Auth {
        uint32 buyValue;
        address owner;
    }

    uint32 public boughtValue;
    uint32 public buyValue;
    mapping(uint256 => Share) public shares;
    uint256 public nShares;
    mapping(uint256 => Auth) authed;
    uint256 nAuthed;
    address public supervisor;

    modifier noBought() {
        if(boughtValue < buyValue) _;
    }

    modifier supervises() {
        if(supervisor == msg.sender) _;
    }

    //Constructor
    function SplitSell(uint256 _buyValue) {
        buyValue = _buyValue;
        supervisor = msg.sender;
    }

    function addAuth(uint32 buyValue, address owner) supervises {
        for(uint256 i = 0; i < nAuthed; i++) {
            if(authed[i].owner == owner) {
                authed[i].buyValue += buyValue;
                return;
            }
        }
        //If not found...
        authed[nAuthed] = Auth(buyValue, owner);
        nAuthed++;
    }

    function _removeAuth(uint256 at) private {
        for(uint256 i = at; i < nAuthed - 1; i++)
            authed[i] = authed[i + 1];
        nAuthed--;
    }

    function _removeShare(uint256 at) private {
        for(uint256 i = at; i < nShares - 1; i++)
            shares[i] = shares[i + 1];
        nShares--;
    }

    function removeAuth(uint32 buyValue, address owner) supervises {
        for(uint256 i = 0; i < nAuthed; i++) {
            if(authed[i].owner == owner) {
                authed[i].buyValue -= buyValue;
                if(authed[i].buyValue <= 0) {
                    _removeAuth(i);
                }
                return;
            }
        }
    }

    function setSupervisor(address now) supervises {
        supervisor = now;
    }

    function buyShare(uint32 buyingValue, bytes32 ownerName, bytes32 ownerRRN) noBought {
        for(uint256 i = 0; i < nAuthed; i++) {
            if(authed[i].owner == msg.sender) {
                uint32 spending = buyingValue > authed[i].buyValue? authed[i].buyValue : buyingValue;
                spending = spending > buyValue - boughtValue? buyValue - boughtValue : spending;
                //Remove
                authed[i].buyValue -= spending;
                if(authed[i].buyValue <= 0) {
                    _removeAuth(i);
                }
                //ACK
                boughtValue += spending;
                if(boughtValue >= buyValue)
                    onBuy();
                //Credit
                for(i = 0; i < nShares; i++) {
                    if(shares[i].owner == msg.sender) {
                        shares[i].buyValue += spending;
                        return;
                    }
                }
                shares[nShares] = Share(spending, msg.sender, ownerName, ownerRRN);
                nShares++;
                return;
            }
        }
    }

    function sellShare(uint32 sellingValue, address to, bytes32 toName, bytes32 toRRN) {
        for(uint256 i = 0; i < nShares; i++) {
            if(shares[i].owner == msg.sender) {
                uint32 spending = sellingValue > shares[i].buyValue? shares[i].buyValue : sellingValue;
                //Remove
                shares[i].buyValue -= spending;
                if(shares[i].buyValue <= 0) {
                    _removeShare(i);
                }
                //Credit
                for(i = 0; i < nShares; i++) {
                    if(shares[i].owner == to) {
                        shares[i].buyValue += spending;
                        return;
                    }
                }
                shares[nShares] = Share(spending, to, toName, toRRN);
                nShares++;
                return;
            }
        }
    }
}