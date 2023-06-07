import React from "react";

import {
  Box,
  AppBar,
  Toolbar,
  IconButton,
  Avatar,
  Typography,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";

const MyAppBar: React.FC = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton>
            <MenuIcon />
          </IconButton>
          <Avatar src="./../../static/favicon.ico"></Avatar>
          <Typography variant="h5" component="div">
            Niffler
          </Typography>
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default MyAppBar;
