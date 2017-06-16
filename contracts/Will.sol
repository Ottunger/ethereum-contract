pragma solidity ^0.4.2;

contract Will {
    struct Config{
        uint256 startDate;
        uint256 endDate;
        uint8 amountHour;
        uint8 hourWeek;
    }

    address public subject; //The guy who has to do
    address public ong; //The ong whose work is done
    mapping(uint256 => address) public sigs; //Other signataires
    uint256 public nSigs; //Number of other signataires
    uint256 public nSigsReq; //Number of signatures amongs the others required to change
    bool public subjectSig;
    bool public ongSig;
    mapping(uint256 => bool) public hasSig; //Has other signed?

    Config public running;
    Config public pending;
    bool isPending;
    uint256 lastProposal;

    modifier noPending() {
        if(!isPending || lastProposal < now - 1 days) _;
    }

    modifier owner() {
        if(msg.sender == subject || msg.sender == ong) _;
    }

    //Constructor
    function Will(bool asSubject, address other, uint256 startDate, uint256 endDate, uint8 amountHour, uint8 hourWeek, uint256 _nSigsReq, address[] _sigs) {
        nSigsReq = _nSigsReq;
        running = Config(0, 0, 0, 0);
        for(; nSigs < _sigs.length; nSigs++) {
            sigs[nSigs] = _sigs[nSigs];
        }

        if(asSubject) {
            subjectSig = true;
            subject = msg.sender;
            ong = other;
        } else {
            ongSig = true;
            subject = other;
            ong = msg.sender;
        }

        propose(startDate, endDate, amountHour, hourWeek);
    }

    function validate() private {
        isPending = false;
        running = pending;
        resetSig();
    }

    function resetSig() private {
        subjectSig = false;
        ongSig = false;
        for(uint256 i = 0; i < nSigs; i++)
            hasSig[i] = false;
    }

    function sign() {
        uint256 count = 0;
        if(msg.sender == subject)
            subjectSig = true;
        if(msg.sender == ong)
            ongSig = true;
        for(uint256 i = 0; i < nSigs; i++)
            if(msg.sender == sigs[i])
                hasSig[i] = true;
        //Check for validity
        if(subjectSig && ongSig) {
            for(i = 0; i < nSigs; i++)
                if(hasSig[i])
                    count++;
            if(count >= nSigsReq)
                validate();
        }
    }

    function propose(uint256 startDate, uint256 endDate, uint8 amountHour, uint8 hourWeek) noPending owner {
        isPending = true;
        lastProposal = now;
        resetSig();
        pending = Config(startDate, endDate, amountHour, hourWeek);
    }

}