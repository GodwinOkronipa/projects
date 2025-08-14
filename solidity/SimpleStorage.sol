// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 private storedValue;

    event ValueChanged(uint256 newValue);

    function set(uint256 newValue) public {
        storedValue = newValue;
        emit ValueChanged(newValue);
    }

    function get() public view returns (uint256) {
        return storedValue;
    }
}
