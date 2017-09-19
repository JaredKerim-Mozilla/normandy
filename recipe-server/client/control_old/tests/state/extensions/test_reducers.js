import { fromJS } from 'immutable';

import {
  EXTENSION_RECEIVE,
} from 'control_old/state/action-types';
import extensionsReducer from 'control_old/state/extensions/reducers';

import {
  INITIAL_STATE,
  EXTENSION,
} from '.';


describe('Extensions reducer', () => {
  it('should return initial state by default', () => {
    expect(extensionsReducer(undefined, {})).toEqual(INITIAL_STATE);
  });

  it('should handle EXTENSION_RECEIVE', () => {
    expect(extensionsReducer(undefined, {
      type: EXTENSION_RECEIVE,
      extension: EXTENSION,
    })).toEqual({
      ...INITIAL_STATE,
      items: INITIAL_STATE.items.set(EXTENSION.id, fromJS(EXTENSION)),
    });
  });
});
