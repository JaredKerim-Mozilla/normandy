import { fromJS } from 'immutable';
import * as matchers from 'jasmine-immutable-matchers';

import {
  APPROVAL_REQUEST_DELETE,
  APPROVAL_REQUEST_RECEIVE,
} from 'control_new/state/action-types';
import approvalRequestsReducer from 'control_new/state/app/approvalRequests/reducers';
import {
  INITIAL_STATE,
  ApprovalRequestFactory,
} from 'control_new/tests/state/approvalRequests';


describe('Approval requests reducer', () => {
  const approvalRequest = ApprovalRequestFactory.build();

  beforeEach(() => {
    jasmine.addMatchers(matchers);
  });

  it('should return initial state by default', () => {
    expect(approvalRequestsReducer(undefined, { type: 'INITIAL' })).toEqual(INITIAL_STATE);
  });

  it('should handle APPROVAL_REQUEST_RECEIVE', () => {
    const reducedApprovalRequest = {
      ...approvalRequest,
      approver_id: approvalRequest.approver ? approvalRequest.approver.id : null,
      creator_id: approvalRequest.creator.id,
    };

    delete reducedApprovalRequest.approver;
    delete reducedApprovalRequest.creator;

    const updatedState = approvalRequestsReducer(undefined, {
      type: APPROVAL_REQUEST_RECEIVE,
      approvalRequest,
    });

    expect(updatedState.items).toEqualImmutable(
      INITIAL_STATE.items.set(approvalRequest.id, fromJS(reducedApprovalRequest)),
    );
  });

  it('should handle APPROVAL_REQUEST_DELETE', () => {
    const state = approvalRequestsReducer(undefined, {
      type: APPROVAL_REQUEST_RECEIVE,
      approvalRequest,
    });

    const updatedState = approvalRequestsReducer(state, {
      type: APPROVAL_REQUEST_DELETE,
      approvalRequestId: approvalRequest.id,
    });

    expect(updatedState).toEqual(INITIAL_STATE);
  });
});
