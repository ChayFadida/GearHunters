import React, { createContext, useContext } from 'react';

const AppContext = createContext();

export const AppProvider = ({ children, routes }) => {
  return (
    <AppContext.Provider value={{ routes }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  return useContext(AppContext);
};
