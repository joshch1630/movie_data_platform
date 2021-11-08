import { render, screen, within } from '@testing-library/react';
import App from '../App';

// Mocking Components
jest.mock('../Components/BehindTheScenesComponent', () => () => (<div>BehindTheScenesComponent</div>));
jest.mock('../Components/DataFlowComponent', () => () => (<div>DataFlowComponent</div>));
jest.mock('../Components/IMDbAnalysisComponent', () => () => (<div>IMDbAnalysisComponent</div>));
jest.mock('../Components/MovieLensAnalysisComponent', () => () => (<div>DataFlowComponent</div>));

describe('Rendering - Top menu bar and side menu', () => {

  test('renders top menu bar', () => {
    render(<App />);

    const expectedElement = screen.getByText('Moive Data Platform');
    expect(expectedElement).toBeInTheDocument();

  });

  test('renders side menu', () => {
    render(<App />);

    let expectedElement = '';

    // Home link
    const link = screen.getByRole('link', {
      name: /home/i
    });
    expectedElement = within(link).getByText(/home/i);
    expect(expectedElement).toBeInTheDocument();

    const navigation = screen.getByRole('navigation');

    // Data FLow link
    expectedElement = within(navigation).getByText(/data flow/i);
    expect(expectedElement).toBeInTheDocument();

    // Data Analysis link
    const button = screen.getByRole('button', {
      name: /data analysis/i
    });
    expectedElement = within(button).getByText(/data analysis/i);
    expect(expectedElement).toBeInTheDocument();

    // Imdb Analysis link
    expectedElement = within(navigation).getByRole('link', {
      name: /imdb analysis/i
    });
    expect(expectedElement).toBeInTheDocument();

    // MovieLens Analysis link
    expectedElement = within(navigation).getByRole('link', {
      name: /movielens analysis/i
    });
    expect(expectedElement).toBeInTheDocument();

    // Behind The Scenes link
    expectedElement = within(navigation).getByRole('link', {
      name: /behind the scenes/i
    });
    expect(expectedElement).toBeInTheDocument();

    // Icons by icon8 link
    expectedElement = screen.getByRole('link', {
      name: /icons by icons8/i
    });
    expect(expectedElement).toBeInTheDocument();

  });

  test('renders home page menu', () => {
    render(<App />);

    let expectedElement = '';

    const main = screen.getByRole('main');

    // Data Flow button
    expectedElement = within(main).getByRole('link', {
      name: /data flow data flow/i
    });
    expect(expectedElement).toBeInTheDocument();

    // IMDb Analysis button
    expectedElement = within(main).getByRole('link', {
      name: /imdb analysis/i
    });
    expect(expectedElement).toBeInTheDocument();

    // MovieLens Analysis button
    expectedElement = within(main).getByRole('link', {
      name: /movielens analysis/i
    });
    expect(expectedElement).toBeInTheDocument();

    // Behind The Scenes button
    expectedElement = within(main).getByRole('link', {
      name: /behind the scenes/i
    });
    expect(expectedElement).toBeInTheDocument();

  });
});
