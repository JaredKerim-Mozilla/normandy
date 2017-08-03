import React, { PropTypes as pt } from 'react';
import { connect } from 'react-redux';

import { ControlField } from 'control/components/Fields';
import ActionFields from 'control/components/action_fields/ActionFields';
import QueryExtensions from 'control/components/data/QueryExtensions';
import { getAllExtensions } from 'control/state/extensions/selectors';


/**
 * Form fields for the opt-out-study action.
 */
class OptOutStudyFields extends ActionFields {
  static propTypes = {
    disabled: pt.bool,
    extensions: pt.array,
  }

  render() {
    const { disabled, extensions } = this.props;
    return (
      <div className="arguments-fields">
        <QueryExtensions />

        <p className="info">Enroll the user in an opt-out SHIELD study</p>

        <ControlField
          disabled={disabled}
          label="Study Name"
          name="arguments.name"
          component="input"
          type="text"
        />

        <ControlField
          disabled={disabled}
          label="Study Description"
          name="arguments.description"
          component="textarea"
        />

        <ControlField
          disabled={disabled}
          label="Add-on"
          name="arguments.addonUrl"
          component="select"
        >
          {extensions.map(extension => (
            <option key={extension.get('id')} value={extension.get('xpi')}>
              {extension.get('name')}
            </option>
          ))}
        </ControlField>
      </div>
    );
  }
}

export default connect(
  state => ({
    extensions: getAllExtensions(state).toArray(),
  }),
)(OptOutStudyFields);
