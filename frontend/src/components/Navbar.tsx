import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
  navigationMenuTriggerStyle,
} from "./ui/navigation-menu";
import { cn } from "../lib/utils";

const Navbar: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <NavigationMenu>
      <NavigationMenuList>
        {isAuthenticated ? (
          <>
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <Link to="/profile" className={navigationMenuTriggerStyle()}>
                  Profile
                </Link>
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <button
                onClick={handleLogout}
                className={cn(navigationMenuTriggerStyle(), "cursor-pointer")}
              >
                Logout
              </button>
            </NavigationMenuItem>
          </>
        ) : (
          <>
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <Link to="/login" className={navigationMenuTriggerStyle()}>
                  Login
                </Link>
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <Link to="/signup" className={navigationMenuTriggerStyle()}>
                  Sign Up
                </Link>
              </NavigationMenuLink>
            </NavigationMenuItem>
          </>
        )}
      </NavigationMenuList>
    </NavigationMenu>
  );
};

export default Navbar;
