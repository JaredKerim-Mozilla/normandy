import { Action, registerAction, registerAsyncCallback } from '../utils';

let seenRecipeIds = [];

/**
 * Used for unit tests only to reset action state.
 */
export function resetAction() {
  seenRecipeIds = [];
}

/**
 * Enrolls a user in an opt-out study, in which we install an add-on which
 * manages branch selection, changes to Firefox, etc.
 */
export default class OptOutStudyAction extends Action {
  async execute() {
    const recipeId = this.recipe.id;
    const { name, description, addonUrl } = this.recipe.arguments;
    const studies = this.normandy.studies;

    // Exit early if we're on an incompatible client.
    if (studies === undefined) {
      this.normandy.log('Client does not support studies, aborting.', 'info');
      return;
    }

    seenRecipeIds.push(recipeId);

    // If the study doesn't exist yet, enroll!
    const hasStudy = await studies.has(recipeId);
    if (!hasStudy) {
      this.normandy.log(`Starting study for recipe ${recipeId}`, 'debug');
      await studies.start({
        recipeId,
        name,
        description,
        addonUrl,
      });
    } else {
      this.normandy.log(`Study for recipe ${recipeId} already exists`, 'debug');
    }
  }
}
registerAction('opt-out-study', OptOutStudyAction);

/**
 * Finds active studies that were not stored in the seenRecipeIds list during
 * action execution, and stops them.
 */
export async function postExecutionHook(normandy) {
  const studies = normandy.studies;

  // Exit early if we're on an incompatible client.
  if (studies === undefined) {
    normandy.log('Client does not support studies, aborting.', 'info');
    return;
  }

  // If any of the active studies were not seen during a run, stop them.
  const activeStudies = (await studies.getAll()).filter(study => study.active);
  for (const study of activeStudies) {
    if (!seenRecipeIds.includes(study.recipeId)) {
      normandy.log('Stopping study for recipe ${study.recipeId}.', 'debug');
      try {
        // eslint-disable-next-line no-await-in-loop
        await studies.stop(study.recipeId);
      } catch (err) {
        normandy.log(`Error while stopping study for recipe ${study.recipeId}: ${err}`, 'error');
      }
    }
  }
}
registerAsyncCallback('postExecution', postExecutionHook);
