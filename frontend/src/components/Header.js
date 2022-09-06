import React, { Component } from 'react';
import '../stylesheets/Header.css';

class Header extends Component {
  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <div className='App-header'>
        <h1
          onClick={() => {
            this.navTo('');
          }}
          style={{"cursor":"pointer"}}
        >
          Udacitrivia
        </h1>
        <h2
          onClick={() => {
            this.navTo('');
          }}
          style={{"cursor":"pointer"}}
        >
          List
        </h2>
        <h2
          onClick={() => {
            this.navTo('/add');
          }}
          style={{"cursor":"pointer"}}
        >
          Add
        </h2>
        <h2
          onClick={() => {
            this.navTo('/play');
          }}
          style={{"cursor":"pointer"}}
        >
          Play
        </h2>
      </div>
    );
  }
}

export default Header;
