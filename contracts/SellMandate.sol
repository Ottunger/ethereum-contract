pragma solidity ^0.4.2;

contract SellMandate {
    event onSigned();

    struct Config{
        uint256 startDate;
        uint256 endDate;
        bytes32 pdfSha3;
        uint32 mandateePrice;
        uint32 buyValue;
    }

    address public mandatee;
    address public mandater;
    bool public mandateeSig;
    bool public mandaterSig;

    Config public running;
    Config public pending;
    bool isPending;
    uint256 lastProposal;

    modifier noPending() {
        if(!isPending || lastProposal < now - 1 days) _;
    }

    modifier owner() {
        if(msg.sender == mandatee || msg.sender == mandater) _;
    }

    //Constructor
    function SellMandate(bool asMandatee, address other, uint256 startDate, uint256 endDate, bytes32 pdfSha3, uint32 mandateePrice, uint32 buyValue) {
        running = Config(0, 0, '', 0, 0);

        if(asMandatee) {
            mandateeSig = true;
            mandatee = msg.sender;
            mandater = other;
        } else {
            mandaterSig = true;
            mandatee = other;
            mandater = msg.sender;
        }

        propose(startDate, endDate, pdfSha3, mandateePrice, buyValue);
    }

    function validate() private {
        isPending = false;
        running = pending;
        resetSig();
        onSigned();
    }

    function resetSig() private {
        subjectSig = false;
        ongSig = false;
    }

    function sign() {
        if(msg.sender == mandatee)
            mandateeSig = true;
        if(msg.sender == mandater)
            mandaterSig = true;
        //Check for validity
        if(mandateeSig && mandaterSig) {
            validate();
        }
    }

    function propose(uint256 startDate, uint256 endDate, bytes32 pdfSha3, uint32 mandateePrice, uint32 buyValue) noPending owner {
        isPending = true;
        lastProposal = now;
        resetSig();
        pending = Config(startDate, endDate, pdfSha3, mandateePrice, buyValue);
    }

    function getAllInfo() constant returns (uint256, uint256, bytes32, uint32, uint32, uint256, uint256, bytes32, uint32, uint32,
            address, address, bool, uint256) {
        return (running.startDate, running.endDate, running.pdfSha3, running.mandateePrice, running.buyValue,
        pending.startDate, pending.endDate, pending.pdfSha3, pending.mandateePrice, pending.buyValue,
        mandatee, mandater, isPending, lastProposal);
    }

}