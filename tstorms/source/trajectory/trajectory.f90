  PROGRAM TRAJECTORY
!===================================================================
!  --- DETECT TROPICAL STORM TRAJECTORIES 
!===================================================================
  use TS_TOOLS_MOD
  implicit none
!-------------------------------------------------------------------

  integer, parameter :: numax    = 5000
  integer, parameter :: nmaxtraj = 5000
  integer, parameter :: lonmax   = 5000
  integer, parameter :: nrmx     = 5000

  integer, parameter :: iucyc = 12
  integer, parameter :: iutra = 13
  integer, parameter :: iuori = 14
  integer, parameter :: iusta = 15

!-------------------------------------------------------------------

  real,  parameter :: RADIUS = 6371.0
  real :: PI, RADIAN
  real :: rlon_0, rlat_0, rlon_i, rlat_i, dx, dy, dr

!-------------------------------------------------------------------

  integer :: iday, jcyc, mdays

  integer, dimension(numax)  :: icand, jcand
  integer, dimension(numax)  :: ix, iy, bon_1, bon_2
  real,    dimension(numax)  :: rtot

  integer :: bon, num_traj, long_traj
  integer :: l, i1, j1,  ncand 
  integer :: inc, nwnd, inc1, nr, m
  integer :: fthick, ftwc
  real    :: pthick, ptwc

  integer, dimension(1) :: imin

!-------------------------------------------------------------------

  integer :: day0, month0, year0, hour0, number0
  integer :: day1, month1, year1, hour1
  integer :: idex, jdex

  real    :: psl_lon,  psl_lat,  wind_max, vort_max, psl_min
  real    :: vort_lon, vort_lat, tbar_lon, tbar_lat, thick_lon, thick_lat  

  logical :: twc_is,  thick_is

  integer, dimension(nrmx)        :: day,  month, year, number, hour
  real,    dimension(nrmx,numax)  :: rlon, rlat,  wind, psl 
  logical, dimension(nrmx,numax)  :: available
  logical, dimension(nrmx,numax)  :: exist_wind, exist_twc, exist_thick

!-------------------------------------------------------------------

  real     ::  rcrit    = 400.0
  !real     ::  wcrit    =  17.0
  real     ::  wcrit    =  15.2
  !integer  :: nwcrit    =   8
  integer  :: nwcrit    =   3
  logical  :: do_filt   = .false. 
  character(100) :: work_dir
  character(100) :: nml_name = "nml_trajectory"
  character(200) :: nml_full


  namelist / nml_trajectory /  rcrit, wcrit, nwcrit, do_filt

!===================================================================

  PI     = 4.0*ATAN(1.0)
  RADIAN = 180.0/PI

 103 FORMAT( 2f8.2,   4i6 )
 104 FORMAT( 'start', 5i6 )
 105 FORMAT( 4f8.2,   4i6 )
 106 FORMAT( 'start', 5i6, 2f8.2)

  CALL GETARG(1,work_dir)
  nml_full = TRIM(work_dir) // "/" // TRIM(nml_name)
  nml_full = TRIM(nml_full)
  OPEN( UNIT = 101, FILE = nml_full )
  READ( 101, nml_trajectory )
  CLOSE( 101 )

  !READ( *, nml_trajectory )

!===================================================================
! --- ETAPE 1:  LECTURE DU FICHIER DE DONNEES
!===================================================================

           rlon(:,:) = 0.0
           rlat(:,:) = 0.0
           wind(:,:) = 0.0
     exist_wind(:,:) = .false.
      exist_twc(:,:) = .false.
    exist_thick(:,:) = .false.
      available(:,:) = .false.

  OPEN( iutra, FILE = TRIM(work_dir) // '/traj', STATUS = 'unknown' )
  OPEN( iuori, FILE = TRIM(work_dir) // '/ori',  STATUS = 'unknown' )

!===================================================================
! --- INPUT DATA
!===================================================================

  OPEN( iucyc, FILE = TRIM(work_dir) // '/cyclones', STATUS = 'unknown' )

  do iday = 1,nrmx
! %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  READ(iucyc,*,end=101) day0, month0, year0, number0, hour0
  WRITE(*,*)      iday, hour0, day0, month0, year0, number0

    number(iday) = number0
      year(iday) = year0
     month(iday) = month0
       day(iday) = day0
      hour(iday) = hour0

  if( number0 > 0 ) then
  do jcyc = 1,number0

    READ(iucyc,*,err=201)  idex,     jdex,              &
                           psl_lon,  psl_lat,           &
                           wind_max, vort_max, psl_min, &
                           twc_is,   thick_is

           rlon(iday,jcyc) = psl_lon
           rlat(iday,jcyc) = psl_lat
            psl(iday,jcyc) = psl_min*0.01
            !psl(iday,jcyc) = psl_min
           wind(iday,jcyc) = wind_max
     exist_wind(iday,jcyc) = ( wind_max >= wcrit )
      exist_twc(iday,jcyc) = twc_is
    exist_thick(iday,jcyc) = thick_is
      available(iday,jcyc) = .true.
      cycle 

      201 continue
      print *, ' BAD DATA AT JCYC: ', jcyc
  
  end do
  end if

! %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  end do

      mdays = iday 
      go to 102
  101 continue
      PRINT *, '*********************************************'
      PRINT *, '  End of file reading record ', iday
      PRINT *, '*********************************************'
      mdays = iday - 1
  102 continue

  CLOSE(iucyc)

!===================================================================
! --- STEP 2: EVALUATION OF TRAJECTORIES
!===================================================================
 
  num_traj  = 0

  do iday = 1,mdays-1
! %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    year0 =  year(iday)
   month0 = month(iday)
     day0 =   day(iday)
    hour0 =  hour(iday)

  do jcyc  = 1,number(iday)
! %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  long_traj = 1
  ix(1)     = iday
  iy(1)     = jcyc

  if( available(iday,jcyc) .and. &
     exist_wind(iday,jcyc) ) then
! %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

      l     = iday + 1
      i1    = iday
      j1    = jcyc
 10   ncand = 0

!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
  if( l > mdays ) go to 999
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

! --- check for candidates on following day

  rlon_0 = rlon(i1,j1) / RADIAN
  rlat_0 = rlat(i1,j1) / RADIAN

  do inc = 1,number(l)
  if( available(l,inc) ) then
  rlon_i = rlon(l,inc) / RADIAN
  rlat_i = rlat(l,inc) / RADIAN

  dx = RADIUS * ( rlon_i - rlon_0 ) * cos(rlat_0) 
  dy = RADIUS * ( rlat_i - rlat_0 )
  dr = sqrt( dx*dx + dy*dy )

  if ( dr <= rcrit ) then
           ncand  = ncand + 1
     icand(ncand) = l
     jcand(ncand) = inc
  end if
  end if
  end do

!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
 999 continue       
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

! --- no more candidate storms
  if( ncand == 0 ) then 
! zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz

! --- check winds; count exist_thick and exist_twc flags

                                       nwnd = 0
                                       fthick = 0
                                       ftwc = 0
  do inc = 1,long_traj
    if( exist_wind(ix(inc),iy(inc)) .and. &
         exist_twc(ix(inc),iy(inc)) .and. &
       exist_thick(ix(inc),iy(inc))  ) nwnd = nwnd + 1

    if( exist_thick(ix(inc),iy(inc)) ) fthick = fthick + 1
    if( exist_twc(ix(inc),iy(inc)) ) ftwc = ftwc + 1
  end do

!--- compute percentage of time steps that passed thickness
!--- and warm core criteria 
  if ( long_traj > 0) then
     pthick = (1.0*fthick)/(1.0*long_traj)
     ptwc = (1.0*ftwc)/(1.0*long_traj)
  end if

  if(( long_traj > 1 ).and.( nwnd  >= nwcrit )) then
! zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
 
   num_traj  = num_traj + 1

! --- output trajectory info

! --- WRITE(iutra,104) long_traj, year0, month0, day0, hour0
      WRITE(iutra,106) long_traj, year0, month0, day0, hour0, pthick, ptwc
    do inc1 = 1,long_traj

         year1 =  year(iday+inc1-1)
        month1 = month(iday+inc1-1)
          day1 =   day(iday+inc1-1)
         hour1 =  hour(iday+inc1-1)

      WRITE(iutra,105) rlon(ix(inc1),iy(inc1)), &
                       rlat(ix(inc1),iy(inc1)), &
                       wind(ix(inc1),iy(inc1)), &
                        psl(ix(inc1),iy(inc1)), &
                       year1, month1, day1, hour1
    end do
 
    WRITE(iuori,103) rlon(ix(1),iy(1)), rlat(ix(1),iy(1)), &
                   year0, month0, day0, hour0

! --- eliminate storms used for this trajectory
  do inc1 = 1,long_traj
     available(ix(inc1),iy(inc1)) = .false.
  end do

! zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
  end if
  end if

! --- one candidate storm
  if( ncand == 1 ) then
! xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
     long_traj  = long_traj + 1
  ix(long_traj) = icand(1)
  iy(long_traj) = jcand(1)

  l  = l + 1
  i1 = ix(long_traj)
  j1 = iy(long_traj)

  goto 10
! xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  end if

! --- more than one candidate storm
  if( ncand > 1 ) then
! xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

  rlon_0 =     rlon(i1,j1)
  rlat_0 = ABS(rlat(i1,j1))

          bon  = 0
  do inc = 1,ncand
      rlon_i =     rlon(l,inc)
      rlat_i = ABS(rlat(l,inc))
  if( rlon_i <= rlon_0 ) then
  if( rlat_i >= rlat_0 ) then
          bon  = bon + 1
    bon_1(bon) = icand(inc)
    bon_2(bon) = jcand(inc)
  end if
  end if
  end do

  if( bon == 1 ) then
! --------------------------------
     long_traj  = long_traj + 1
  ix(long_traj) = bon_1(1)
  iy(long_traj) = bon_2(1)

  l  = l + 1
  i1 = ix(long_traj)
  j1 = iy(long_traj)

  goto 10
! --------------------------------
  end if

  if ( bon >= 2 ) then
! --------------------------------
  do inc = 1,bon
    dx = ( rlon(bon_1(inc),bon_2(inc)) - rlon(i1,j1) )
    dy = ( rlat(bon_1(inc),bon_2(inc)) - rlat(i1,j1) )
    rtot(inc) = sqrt( dx*dx + dy*dy )
  end do

  imin = MINLOC( rtot(1:bon) )

       long_traj  = long_traj + 1
    ix(long_traj) = bon_1(imin(1))
    iy(long_traj) = bon_2(imin(1))
    l  = l + 1
    i1 = ix(long_traj)
    j1 = iy(long_traj)
  goto  10
! --------------------------------
  end if

  if( bon == 0 ) then
! --------------------------------
  do inc = 1,ncand
    dx = ( rlon(icand(inc),jcand(inc)) - rlon(i1,j1) )
    dy = ( rlat(icand(inc),jcand(inc)) - rlat(i1,j1) )
    rtot(inc) = sqrt( dx*dx + dy*dy )
  end do

  imin = MINLOC( rtot(1:ncand) )

       long_traj  = long_traj + 1
    ix(long_traj) = icand(imin(1))
    iy(long_traj) = jcand(imin(1))
    l  = l + 1
    i1 = ix(long_traj)
    j1 = iy(long_traj)
  goto  10
! --------------------------------
  endif

! xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  end if

! %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  end if
  end do
  end do

!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
! 999 continue
!     print *, ' STOP 999'
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

  CLOSE( iutra )
  CLOSE( iuori )

!===================================================================
! --- FILTER DATA
!===================================================================

  if( do_filt ) CALL TS_FILTER3( work_dir )

!===================================================================
! --- STATS
!===================================================================
 
  CALL TS_STATS ( do_filt, work_dir )

!===================================================================
  end PROGRAM TRAJECTORY
