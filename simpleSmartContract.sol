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
    
