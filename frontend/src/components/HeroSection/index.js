import React, { useState } from 'react';
import Video from '../../videos/video.mp4';
import { Button } from '../../utils/ButtonElement';
import { Link } from "react-router-dom";import {
  HeroContainer,
  HeroBg,
  VideoBg,
  HeroContent,
  HeroH1,
  HeroP,
  HeroBtnWrapper,
  ArrowForward,
  ArrowRight 
} from './HeroElements';

const HeroSection = () => {
  const [hover, setHover] = useState(false)

  const onHover = () => {
    setHover(!hover)
  }

  return (
    <HeroContainer>
        <HeroBg>
            <VideoBg autoPlay loop muted src={Video} type='video/mp4' />
        </HeroBg>
        <HeroContent>
          <HeroH1>Hype Beast Dashboard</HeroH1>
          <HeroP>
            Welcome, this is a website to better understand the
            shoe resale market on Ebay, GOAT, StockX!
          </HeroP>
          <Button
            onMouseEnter={onHover}
            onMouseLeave={onHover}
            primary='true'
            dark='true'
          >
            <Link to="/analytics">Get Started</Link> {hover ? <ArrowForward /> : <ArrowRight />}
          </Button>
        </HeroContent>
    </HeroContainer>
  )
}

export default HeroSection