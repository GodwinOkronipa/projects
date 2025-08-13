// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// This is our improved smart contract for storing a name.
contract SimpleStorage {
    // This state variable will store the owner's address.
    address private owner;
    
    // This state variable will store the name.
    string public myName;
    
    // This event will be emitted whenever the name is changed.
    event NameChanged(string oldName, string newName);

    
    // This is a special function called a constructor. It runs only once when the contract is deployed.
    constructor() {
        owner = msg.sender;
    }
    
    // This function sets the value of our name.
    // The `onlyOwner` modifier ensures only the owner can call this function.
    function setName(string memory newName) public onlyOwner {
        string memory oldName = myName;
        myName = newName;
        // Emit the event to notify listeners of the change.
        emit NameChanged(oldName, newName);
    }
    
    // This is our custom modifier for access control.securing the contract
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function.");
        _;
    }
}
    
