import { Card } from 'antd';
import { Map } from 'immutable';
import PropTypes from 'prop-types';
import React from 'react';


export default class RecipeDetails extends React.Component {
  static propTypes = {
    recipe: PropTypes.instanceOf(Map).isRequired,
  }

  render() {
    const { recipe } = this.props;

    return (
      <div className="recipe-details">
        <Card key="recipe-details" title="Recipe">
          <dl className="details">
            <dt>Name</dt>
            <dd>{recipe.get('name')}</dd>

            <dt>Filters</dt>
            <dd>
              <pre><code>{recipe.get('extra_filter_expression')}</code></pre>
            </dd>
          </dl>
        </Card>

        <Card key="action-details" title="Action">
          <dl className="details">
            <dt>Name</dt>
            <dd>{recipe.getIn(['action', 'name'])}</dd>

            {
              recipe.get('arguments', new Map()).map((value, key) => ([
                <dt key={`dt-${key}`}>
                  {key.replace(/([A-Z]+)/g, ' $1')}
                </dt>,
                <dd key={`dd-${key}`}>
                  {value}
                </dd>,
              ])).toArray()
            }
          </dl>
        </Card>
      </div>
    );
  }
}
