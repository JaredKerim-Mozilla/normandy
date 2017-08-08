import { message } from 'antd';
import autobind from 'autobind-decorator';
import { Map } from 'immutable';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import LoadingOverlay from 'control_new/components/common/LoadingOverlay';
import QueryExtension from 'control_new/components/data/QueryExtension';
import ExtensionForm from 'control_new/components/extensions/ExtensionForm';
import {
  updateExtension as updateExtensionAction,
} from 'control_new/state/app/extensions/actions';
import { getExtension } from 'control_new/state/app/extensions/selectors';
import { getUrlParamAsInt } from 'control_new/state/router/selectors';


@connect(
  state => {
    const extensionId = getUrlParamAsInt(state, 'extensionId');
    const extension = getExtension(state, extensionId, new Map());
    return {
      extension,
      extensionId,
    };
  },
  {
    updateExtension: updateExtensionAction,
  },
)
@autobind
export default class EditExtensionPage extends React.Component {
  static propTypes = {
    extension: PropTypes.instanceOf(Map).isRequired,
    extensionId: PropTypes.number.isRequired,
    updateExtension: PropTypes.func.isRequired,
  }

  state = {
    formErrors: {},
  };

  /**
   * Update the existing extension and display a message.
   */
  async handleSubmit(values) {
    const { extensionId, updateExtension } = this.props;
    try {
      await updateExtension(extensionId, values);
      message.success('Extension saved');
    } catch (error) {
      message.error(
        'Extension cannot be saved. Please correct any errors listed in the form below.',
      );
      if (error.data) {
        this.setState({ formErrors: error.data });
      }
    }
  }

  render() {
    const { extension, extensionId } = this.props;
    const { formErrors } = this.state;
    return (
      <div>
        <QueryExtension pk={extensionId} />

        <h2>Edit Extension</h2>

        <LoadingOverlay>
          <ExtensionForm
            extension={extension}
            onSubmit={this.handleSubmit}
            errors={formErrors}
          />
        </LoadingOverlay>
      </div>
    );
  }
}
