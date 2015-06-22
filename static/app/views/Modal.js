import React from 'react';
import cx from 'classnames';


/**
 * @class Modal
 * @extends React.Component
 */
export default class Modal extends React.Component {

  static propTypes = {
    children: React.PropTypes.element,
    className: React.PropTypes.string
  };

  static defaultProps = {
    className: ''
  };

  render() {
    return (
      <div className={cx('modal', this.props.className)}>
        <div className="modal--content">
          {this.props.children}
        </div>
      </div>
    );
  }

}
